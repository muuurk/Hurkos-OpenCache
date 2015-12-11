#!/bin/bash

sudo rm /var/lib/mongodb/mongod.lock
sudo mongod --repair -f /etc/mongod.conf
sudo mongod -f /etc/mongod.conf&

echo Javítás kész
clear

