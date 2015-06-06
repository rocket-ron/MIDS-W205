import urllib
import csv
import os
import sys
from pandas import DataFrame, read_csv
import pandas as pd 



# 1) Downloads the dataset from http://www.exploredata.net/ftp/WHO.csv

url = 'http://www.exploredata.net/ftp/WHO.csv'

# 2) Creates a new dataset called 10-40.csv by extracting the records for country ids 
# 10 to 40 and saves the result back on S3 in a bucket called "sub-datasets"

df = pd.read_csv(url)
df[df['CountryID'].isin(range(10,40))].to_csv('10-40.csv', index=False, header=False)

from boto.s3.connection import S3Connection
from boto.s3.key import Key

conn = S3Connection('AKIAJBRIUWSXGQ4NKQTA', 'tlr8toOkSkOB+GD9XmHoX2WQ5Y9sdl5E5EIDYFbU')
bucket = conn.create_bucket('rcordell-sub-datasets')

def percent_cb(complete, total):
	sys.stdout.write('.')
	sys.stdout.flush()


myKey = Key(bucket)
myKey.key = '10-40.csv'
myKey.set_contents_from_filename('10-40.csv', cb=percent_cb)

# 3) Finds the range of values in each column in the original dataset
dfrange = df.select_dtypes(include=['int','float']).max() - df.select_dtypes(include=['int','float']).min()

print dfrange

#4) Finds the county with the minimum Adult mortality rate (probability of dying between 15 to 60 years per 1000 population) male)

index = df['Adult mortality rate (probability of dying between 15 to 60 years per 1000 population) male'].idxmax()
print df.loc[index,'Country']