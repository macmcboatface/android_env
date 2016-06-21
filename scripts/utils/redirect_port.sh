#!/bin/sh
echo "redirecting port $2 on $1 to $3"
sudo iptables -t nat -A PREROUTING -i $1 -p tcp --dport $2 -j REDIRECT --to-port $3
