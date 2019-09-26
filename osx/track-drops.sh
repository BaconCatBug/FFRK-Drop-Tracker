#!/bin/sh
echo "FFRK Drop Tracker"
echo "Use the following IP Address for your proxy: "
./ip_address.sh

./ip_address.sh | xargs -I{} mitmdump -q --listen-host {} --listen-port 8888 -s ../FFRK_Drop_Tracker_v3.16.py
