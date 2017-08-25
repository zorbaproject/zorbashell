#!/bin/bash

tmpfile='/tmp/'$(date +%d%m%Y%H%M%S)'.jpeg'
streamer -s 1280x720 -f jpeg -o $tmpfile  > /dev/null 2>&1
if [ -f $tmpfile ] ; then
echo "photo://"$tmpfile
fi
