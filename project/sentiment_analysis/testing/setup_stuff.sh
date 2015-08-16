#!/bin/bash

cd ~/
curl -o W205-virtualenv.tar.gz http://w205-rcordell-project-setup.s3.amazonaws.com/W205-virtualenv.tar.gz
tar -xzf W205-virtualenv.tar.gz 
. ./W205/bin/activate
