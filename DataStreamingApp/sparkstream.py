from pyspark.sql.session import SparkSession
from pyspark.sql.functions import *
# from dbLoad import ConnectDatabase
import psycopg2
import re
from IPython.display import display
import pandas as pd
from pyspark.sql.types import DateType, TimestampType



spark = SparkSession.builder \
    .master("spark://pntloi:7077") \
    .config("spark.dynamicAllocation.executorIdleTimeout", "600s") \
    .appName("KafkaStreaming").getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "youtube_videos").load()
print("\n\n000000000000000000000000000000000000000000")

df1 = df.selectExpr("CAST(value as STRING)")
# print("\n\n11111111111111111111111111111111111111111111")
# df1.printSchema()
# print("\n\n222222222222222222222222222222222222222222")


# df1.writeStream.format("console").option("truncate", "false").start().awaitTermination()


df2 = df1.withColumn("value_split1", split(col("value"),", \"")) \
    .withColumn("prevideo_id", split(col("value_split1")[0], ": ")) \
    .withColumn("video_id", col("prevideo_id").getItem(1)) \
    .withColumn("pretitle", split(col("value_split1")[1], ": ")) \
    .withColumn("title", col("pretitle").getItem(1)) \
    .withColumn("previews", split(col("value_split1")[2], ": ")) \
    .withColumn("views", col("previews").getItem(1).cast("Integer")) \
    .withColumn("precomments", split(col("value_split1")[3], ": ")) \
    .withColumn("comments", col("precomments").getItem(1).cast("Integer")) \
    .withColumn("prelikes", split(col("value_split1")[4], ": ")) \
    .withColumn("likes", col("prelikes").getItem(1).cast("Integer")) \
    .withColumn("predates", split(col("value_split1")[5], ": ")) \
    .withColumn("dates_brackets", split(col("predates")[1],"}")) \
    .withColumn("dates", col("dates_brackets").getItem(0)) \
    .withColumn("dates", substring(col('dates'), 2, 19) ) \
    .withColumn("dates", to_timestamp(col("dates"))) \
    .drop("value_split1", "value", "prevideo_id", "pretitle", "previews", "precomments", "prelikes","dates_brackets", "predates")

# df3 = df2.withColumn("dates", col("dates").cast("timestamp"))

df2.printSchema()

# df2.writeStream.format("console").option("truncate", "false").start().awaitTermination()

def ConnectDatabase(row):
    HOSTNAME="localhost"
    DATABASE="airflow"
    PORT=5432
    USER="airflow"
    PASSWORD="airflow"
    DBTABLE="youtube_videos"
    try:
        conn = psycopg2.connect(
            host=HOSTNAME,
            database=DATABASE,
            port=PORT,
            user=USER,
            password=PASSWORD
        )
        cur = conn.cursor()

        sql=f"INSERT INTO {DBTABLE} (video_id, title, views, comments, likes, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
        val=(row['video_id'], row['title'], row['views'], row['comments'], row['likes'], row['dates'])
        
        cur.execute(sql, val)
        print(cur)
        # return cur
        conn.commit()
        conn.close()
        cur.close()

    except(Exception, psycopg2.DatabaseError) as e:
        print(e)


df2.printSchema()
df2.describe()
df2.writeStream.format("console").option("truncate", "false").outputMode("append").start()
df2.writeStream.outputMode("update").foreach(ConnectDatabase).start().awaitTermination(timeout=1000)





