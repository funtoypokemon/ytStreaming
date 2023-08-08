import pyspark
from pyspark.sql.session import SparkSession
# import org.apache.spark.sql.hive.HiveContext

spark = SparkSession.builder.appName("Spark_Hive_Integration") \
    .master("local[*]") \
    .config("spark.sql.warehouse.dir", "../data/hive") \
    .config("spark.sql.hive.hiveserver2.jdbc.url", "thrift://192.168.128.178:9083") \
    .enableHiveSupport() \
    .getOrCreate()

spark.sql("use hadoop_ytstreaming;")


df = spark.sql("select * from ytstreaming_warehouse;")


df.printSchema()
df.show()