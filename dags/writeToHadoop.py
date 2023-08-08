import airflow
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.contrib.operators.ssh_operator import SSHOperator


# sshHook = SSHHook(ssh_conn_id='tolocalhost')


Dag_name = "PostgresToHDFS"

args = {
    'owner': 'Kenkebabs',
    'start_date': days_ago(1),
    'retries': 1,
}

dag_project = DAG(dag_id=Dag_name, default_args=args,schedule_interval="@daily")





sourceEnv = SSHOperator(ssh_conn_id='tolocalhost',
    task_id = "sourceEnv",
    command = "source ~/.bashrc",
    dag = dag_project
)

streamingConsumer = SSHOperator(ssh_conn_id='tolocalhost',
    task_id = "streamingConsumer",
    command = "/opt/spark/bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1 /home/pntloi/Documents/wholetool/DataStreamingApp/sparkstream.py",
    dag = dag_project,
    cmd_timeout = 7200
)

streamingProducer = SSHOperator(ssh_conn_id='tolocalhost',
    task_id = "streamingProducer",
    command = "python3 /home/pntloi/Documents/wholetool/DataStreamingApp/youtube_watcher.py",
    dag = dag_project,
    cmd_timeout = 7200
)

writeToHDFS = SSHOperator(ssh_conn_id='tolocalhost',
    task_id = "writeToHDFS",
    command = "/opt/spark/bin/spark-submit /home/pntloi/Documents/wholetool/DataStreamingApp/ytVidSqoop.py",
    dag = dag_project
)


getDataToHive = SSHOperator(ssh_conn_id='tolocalhost',
    task_id = "getDataToHive",
    command = "/opt/hadoop/bin/hdfs dfs -copyToLocal hdfs://localhost:9001/pntloi/test/* /home/pntloi/Documents/wholetool/data/hive"                            ,
    dag = dag_project
)

sourceEnv >> [streamingConsumer, streamingProducer] >> writeToHDFS >> getDataToHive