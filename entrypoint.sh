#!/bin/bash
. "/opt/spark/bin/load-spark-env.sh"

# When the spark work_load is master run class org.apache.spark.deploy.master.Master
if [ "$WORKLOAD" == "master" ];
then
export SPARK_MASTER_HOST=`hostname`
cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT >> $SPARK_MASTER_LOG

elif [ "$WORKLOAD" == "worker" ];
then
# When the spark work_load is worker run class org.apache.spark.deploy.master.Worker
cd /opt/spark/bin && ./spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER >> $SPARK_WORKER_LOG

elif [ "$WORKLOAD" == "submit" ];
then
    echo "SPARK SUBMIT"

# elif [ "$WORKLOAD" == "namenode" ];
# then
# /opt/hadoop/bin/hdfs namenode

# elif [ "$WORKLOAD" == "datanode" ];
# then
# /opt/hadoop/bin/hdfs datanode

# elif [ "$WORKLOAD" == "resourcemanager" ];
# then
# /opt/hadoop/bin/yarn resourcemanager

# elif [ "$WORKLOAD" == "nodemanager" ];
# then
# /opt/hadoop/bin/yarn nodemanager

# elif [ "$WORKLOAD" == "zookeeper" ];
# then
# /opt/zookeeper/bin/zkServer.sh start

# elif [ "$WORKLOAD" == "kafka" ];
# then
# /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties

else 
    echo "Please specify workload type"
fi




