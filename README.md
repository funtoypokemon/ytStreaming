###### Version
Hadoop 3.3.6
Kafka 2.12-3.5.0
Spark/PySpark 3.4.1

####Hadoop
# start ssh server
/etc/init.d/ssh start

# format namenode
$HADOOP_HOME/bin/hdfs namenode -format

# start hadoop
$HADOOP_HOME/sbin/start-dfs.sh
$HADOOP_HOME/sbin/start-yarn.sh

List dir: hdfs dfs -ls /

hdfs dfs -mkdir /pntloi/youtube_videos
hdfs dfs -ls /pntloi


####ZK
$ZK_HOME/bin/zkServer.sh start

####Kafka
$KAFKA_HOME/bin/kafka-server-start.sh $KAFKA_HOME/config/server.properties

#####SPARK
start-master.sh
nano /opt/spark/logs/spark-pntloi-org.apache.spark.deploy.master.Master-1-pntloi.out

start-worker.sh <masterUrl>

# KafkaSpark to stream data
spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 sparkstream.py





