#!/bin/bash

api_key=2bae278473b612eaade4c76730fa5231

url_cpu_temp=http://api.yeelink.net/v1.0/device/5101/sensor/7840/datapoints
url_cpu_load=http://api.yeelink.net/v1.0/device/5101/sensor/7841/datapoints
url_mem_load=http://api.yeelink.net/v1.0/device/5101/sensor/7842/datapoints
url_disk_usage=http://api.yeelink.net/v1.0/device/5101/sensor/7843/datapoints
url_traffic_in=http://api.yeelink.net/v1.0/device/5101/sensor/7844/datapoints
url_traffic_out=http://api.yeelink.net/v1.0/device/5101/sensor/7845/datapoints

eval `tsar --rpi --cpu --mem --traffic --partition -s util,bytin,bytout -D --check | awk '{print $3,$4,$5,$6,$7,$9}' | sed -e 's/:/_/g' | sed -e 's/ /\n/g' | sed -e 's/\//r/g'`

traffic_bytin=${traffic_bytin/\.*}
traffic_bytin=`expr $traffic_bytin / 1000`
traffic_bytout=${traffic_bytout/\.*}
traffic_bytout=`expr $traffic_bytout / 1000`

curl --request POST --data "{\"value\":$rpi_temp}" --header "U-ApiKey: $api_key" $url_cpu_temp
curl --request POST --data "{\"value\":$cpu_util}" --header "U-ApiKey: $api_key" $url_cpu_load
curl --request POST --data "{\"value\":$mem_util}" --header "U-ApiKey: $api_key" $url_mem_load
curl --request POST --data "{\"value\":$partition_r_util}" --header "U-ApiKey: $api_key" $url_disk_usage
curl --request POST --data "{\"value\":$traffic_bytin}" --header "U-ApiKey: $api_key" $url_traffic_in
curl --request POST --data "{\"value\":$traffic_bytout}" --header "U-ApiKey: $api_key" $url_traffic_out
