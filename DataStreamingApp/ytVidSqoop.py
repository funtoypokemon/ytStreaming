import pyspark
from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.types import *



spark = SparkSession.builder\
    .config("spark.jars", "/opt/spark/jars/postgresql-42.6.0.jar") \
    .config('spark.driver.extraClassPath', '/opt/spark/jars/postgresql-42.6.0.jar') \
    .appName("SqoopReplacement").master("spark://pntloi:7077") \
    .getOrCreate()


customSchema = StructType([
    StructField("video_id", StringType(), True),
    StructField("title", StringType(), True),
    StructField("views", IntegerType(), True),
    StructField("comments", IntegerType(), True),
    StructField("likes", IntegerType(), True),
    StructField("updated_at", DateType(), True)
])

jdbcDF = spark.read.format('jdbc') \
    .option("driver", "org.postgresql.Driver") \
    .option("url", "jdbc:postgresql://localhost:5432/airflow") \
    .option("dbtable", "youtube_videos") \
    .option("user", "airflow") \
    .option("password", "airflow") \
    .schema(customSchema) \
    .load()



jdbcDF.printSchema()
jdbcDF.show(truncate=False)


jdbcDF.write.partitionBy('updated_at').mode("append").csv("hdfs://localhost:9001/pntloi/test")








