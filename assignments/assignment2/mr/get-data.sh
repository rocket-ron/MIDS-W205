#!/bin/bash
mkdir -p tweets/json/chunks/

chunkfiles=(
      'd9719c65-291a-4cd4-9c78-55eca5801f29-20150617004028.json'
      '523beea8-c95f-41d1-82cb-fd6e1514cbf9-20150617024100.json'
      '000981a9-cb5d-4f63-a418-c2e96a5b1ae2-20150617084710.json'
   );

for f in ${chunkfiles[@]}
do
  echo "Downloading $f ..."
  echo "---"
  aws s3 cp s3://w205-assignment2-rc-0000/$f tweets/json/chunks/. 
done
