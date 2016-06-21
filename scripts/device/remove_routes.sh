#!/system/bin/sh
while read line
do
	ip route delete $line	
done 
