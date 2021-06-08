#!/bin/bash
filename=$1
mp4=".mp4"
vmp4="_video.mp4"
amp4="_audio.mp4" 
while read -r line; 
do 
	id=$(echo $line | sed -e 's/[^0-9]//g')
	if [ ! -f "$id$mp4" ] 
	then 
		/home/kwfu/py/fbvideo_download.py "$line"
		/usr/bin/ffmpeg -nostdin -loglevel error -i "$id$vmp4" -i "$id$amp4" -c copy "$id$mp4"
		if [ -f "$id$mp4" ]; 
		then
			echo "Output: $id$mp4"
			rm "$id$vmp4"
			rm "$id$amp4"
		else
			echo "Output error"
		fi
		sleep 10; 
	fi 
done < $filename
