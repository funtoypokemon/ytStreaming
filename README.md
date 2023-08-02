# Version
Hadoop 3.3.6 
Kafka 2.12-3.5.0
Spark/PySpark 3.4.1

## Start airflow, postgres, redis, hive
docker-compose up airflow-init
docker-compose up -d


# Hadoop
## start ssh server
/etc/init.d/ssh start

## format namenode
$HADOOP_HOME/bin/hdfs namenode -format

# start hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

List dir: hdfs dfs -ls /

hdfs dfs -mkdir /pntloi/youtube_videos
hdfs dfs -ls /pntloi


## ZK
$ZK_HOME/bin/zkServer.sh start

## Kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

## SPARK
start-master.sh
nano /opt/spark/logs/spark-pntloi-org.apache.spark.deploy.master.Master-1-pntloi.out

start-worker.sh <masterUrl>

## KafkaSpark to stream data
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 sparkstream.py


## Hive
hive
!connect jdbc:hive2://hiveserver2:10000/
username: airflow
passwd: airflow


create database hadoop_ytstreaming;
show databases;
use hadoop_ytstreaming;

#Copy data to hive mounted dir
hdfs dfs -copyToLocal hdfs://localhost:9001/pntloi/test/* /home/pntloi/Documents/wholetool/data/hive



