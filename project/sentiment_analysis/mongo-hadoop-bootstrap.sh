#!/bin/sh

wget --no-check-certificate -P /home/hadoop/lib https://oss.sonatype.org/content/repositories/releases/org/mongodb/mongodb-driver/3.0.3/mongodb-driver-3.0.3.jar


# Edit this path to point to the location of the jar you're using.
wget --no-check-certificate -P /home/hadoop/lib https://github.com/mongodb/mongo-hadoop/releases/download/r1.4.0/mongo-hadoop-core-1.4.0.jar

wget --no-check-certificate -P /home/hadoop/lib https://github.com/mongodb/mongo-hadoop/releases/download/r1.4.0/mongo-hadoop-streaming-1.4.0.jar



