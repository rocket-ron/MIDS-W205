#!/bin/bash

cd ~/
hadoop fs -get s3n://w205-rcordell-project-setup/W205-virtualenv.tar.gz
tar -xzf W205-virtualenv.tar.gz
. ./W205-virtualenv/bin/activate
