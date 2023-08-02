# Postgres
psql -U airflow -W

## Create db
create database deprojects;
\l
exit
psql -d deprojects -U airflow -W

## Create table
create table if not exists youtube_videos(
video_id varchar(150) primary key,
title varchar(150),
views integer,
comments integer,
likes integer);


# Kafka
Kafka topics = 'youtube_videos'
partitions = 1
value format = 'avro'