FROM ubuntu:focal


ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Ho_Chi_Minh
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get update
RUN apt-get install -y tzdata
RUN apt-get update && apt-get install -y wget python3 software-properties-common python3-pip 
RUN pip3 install --upgrade pip
RUN pip3 install pyspark==3.4.0
RUN add-apt-repository ppa:openjdk-r/ppa
RUN apt-get update
RUN apt install -y openjdk-11-jdk
RUN apt-get install -y curl

# Download packages
RUN wget --no-verbose -O apache-spark.tgz "https://dlcdn.apache.org/spark/spark-3.4.0/spark-3.4.0-bin-hadoop3.tgz"
RUN curl -s https://dlcdn.apache.org/hadoop/common/hadoop-3.3.6/hadoop-3.3.6.tar.gz | tar -xz -C /opt/
# RUN curl -s https://dlcdn.apache.org/hive/hive-4.0.0-alpha-2/apache-hive-4.0.0-alpha-2-bin.tar.gz | tar -xz -C /opt/
RUN curl -s https://dlcdn.apache.org/zookeeper/zookeeper-3.7.1/apache-zookeeper-3.7.1-bin.tar.gz | tar -xz -C /opt/
RUN wget --no-verbose -O kafka.tgz "https://downloads.apache.org/kafka/3.5.0/kafka_2.12-3.5.0.tgz"

RUN apt-get install openssh-client openssh-server -y
RUN /etc/init.d/ssh start

# Spark config
RUN mkdir -p /opt/spark
RUN tar -xzvf apache-spark.tgz -C /opt/spark --strip-components=1
RUN rm apache-spark.tgz

WORKDIR /opt/spark

RUN mkdir -p /opt/spark/logs && \
touch /opt/spark/logs/spark-master.out && \
touch /opt/spark/logs/spark-worker.out && \
ln -sf /dev/stdout /opt/spark/logs/spark-master.out && \
ln -sf /dev/stdout /opt/spark/logs/spark-worker.out

COPY start-spark.sh /



# Hadoop config

RUN apt-get update && apt-get install -y ssh rsync nano 
WORKDIR /opt
RUN pwd
RUN mv ./hadoop* hadoop 

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
chmod 0600 ~/.ssh/authorized_keys

COPY /config/config /root/.ssh/config
RUN ls /root/.ssh 
# RUN ssh-keygen -q -t rsa -N '' -f /id_rsa
# RUN mkdir -p ~/.ssh/
# RUN cp /id_rsa ~/.ssh/id_rsa
# COPY /id_rsa.pub /id_rsa.pub
# RUN cp /id_rsa.pub ~/.ssh/id_rsa.pub
# RUN mv /.ssh/id_rsa.pub /.ssh/authorized_keys
WORKDIR /opt/hadoop
COPY /config/hadoop/core-site.xml /opt/hadoop/etc/hadoop/core-site.xml
COPY /config/hadoop/yarn-site.xml /opt/hadoop/etc/hadoop/yarn-site.xml
COPY /config/hadoop/hdfs-site.xml /opt/hadoop/etc/hadoop/hdfs-site.xml
COPY /config/hadoop/mapred-site.xml /opt/hadoop/etc/hadoop/mapred-site.xml
COPY /config/hadoop/hadoop-env.sh /opt/hadoop/etc/hadoop/hadoop-env.sh

###Namenode
EXPOSE 8020 9870 
###Resource manager
EXPOSE 8088 


# # Hive config
# RUN cd /opt/
# RUN mv ./apache-hive* hive 
# RUN cd $HIVE_HOME/conf
# RUN cp hive-env.sh.template hive-env.sh


# ZK config
WORKDIR /opt
RUN mv ./apache-zookeeper* zookeeper 
COPY /config/zookeeper/zoo.cfg /opt/zookeeper/conf/zoo.cfg
EXPOSE 2181


# Kafka config
WORKDIR /
RUN mkdir -p /opt/kafka
RUN tar -xzvf kafka.tgz -C /opt/kafka --strip-components=1
RUN rm kafka.tgz
EXPOSE 9092



COPY /.env /.env
RUN cat /.env >> ~/.bashrc
COPY /entrypoint.sh /

ENV JAVA_HOME=/usr/lib/jvm/java-1.11.0-openjdk-amd64 \
SPARK_VERSION=3.4.0 \
HADOOP_VERSION=3.3.6 \
SPARK_HOME=/opt/spark \
PYTHONHASHSEED=1 \
SPARK_MASTER_PORT=7077 \
SPARK_MASTER_WEBUI_PORT=8090 \
SPARK_LOG_DIR=/opt/spark/logs \
SPARK_MASTER_LOG=/opt/spark/logs/spark-master.out \
SPARK_WORKER_LOG=/opt/spark/logs/spark-worker.out \
SPARK_WORKER_WEBUI_PORT=8090 \
SPARK_WORKER_PORT=7000 \
SPARK_MASTER="spark://spark-master:7077" \
SPARK_WORKLOAD="master" \
HADOOP_HOME=/opt/hadoop \
HADOOP_MAPRED_HOME=$HADOOP_HOME \
HADOOP_COMMON_HOME=$HADOOP_HOME \
HADOOP_HDFS_HOME=$HADOOP_HOME \
YARN_HOME=$HADOOP_HOME \
HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native \
HADOOP_INSTALL=$HADOOP_HOME \
HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop \
HADOOP_LOG_DIR=$HADOOP_HOME/logs \
PDSH_RCMD_TYPE=ssh \
HADOOP_OPTS="-Djava.library.path=$HADOOP_HOME/lib/native" \
ZK_HOME=/opt/zookeeper \
KAFKA_HOME=/opt/kafka \
HDFS_NAMENODE_USER="root" \
HDFS_DATANODE_USER="root" \
HDFS_SECONDARYNAMENODE_USER="root" \
YARN_RESOURCEMANAGER_USER="root" \
YARN_NODEMANAGER_USER="root" \
PATH=$PATH:$JAVA_HOME/bin:$SPARK_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$ZK_HOME/bin:$KAFKA_HOME/bin


CMD ["/bin/bash", "/entrypoint.sh"]