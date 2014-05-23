#!/bin/bash

#Install IMP
cd /root/YCSB
yum install -y python3-setuptools python3-amqplib python3-tornado \
      python3-dateutil python3-apsw python3-execnet python3-plyvel git
git clone https://github.com/bartv/imp
cd imp
python3 setup.py install
