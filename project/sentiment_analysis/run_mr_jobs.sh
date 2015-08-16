#!/bin/sh
#python fear_timeseries.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/timeseries/ebola s3://w205-rcordell-project/data/ebola.json &> ebola_timeseries.out

#python fear_timeseries.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/timeseries/isis s3://w205-rcordell-project/data/isis.json &> isis_timeseries.out

#python fear_timeseries.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/timeseries/greece s3://w205-rcordell-project/data/greece.json &> greece_timeseries.out

#python fear_timeseries.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/timeseries/immigration s3://w205-rcordell-project/data/immigration.json &> immigration_timeseries.out

#python fear_timeseries.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/timeseries/trump s3://w205-rcordell-project/data/trump.json &> trump_timeseries.out

python fear_count.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/fearcounts/ebola_userid s3://w205-rcordell-project/data/ebola.json &> ebola_fearcounts.out

python fear_count.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/fearcounts/isis_userid s3://w205-rcordell-project/data/isis.json &> isis_fearcounts.out

python fear_count.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/fearcounts/greece_userid s3://w205-rcordell-project/data/greece.json &> greece_fearcounts.out

python fear_count.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/fearcounts/immigration_userid s3://w205-rcordell-project/data/immigration.json &> immigration_fearcounts.out

python fear_count.py -r emr --conf-path mrjob.conf --cleanup NONE --no-output --output-dir s3://w205-rcordell-project/emr/output/fearcounts/trump_userid s3://w205-rcordell-project/data/trump.json &> trump_fearcounts.out
