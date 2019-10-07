#!/bin/sh
echo "FFRK Inventory Exporter"
echo "Use the following IP Address for your proxy: "
./ip_address.sh

./ip_address.sh | xargs -I{} mitmdump -q --listen-host {} --listen-port 8888 -s ../FFRK_Inventory_Exporter_v3.16.py
