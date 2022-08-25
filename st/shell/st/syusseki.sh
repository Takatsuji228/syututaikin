#!/bin/bash

truncate syusseki.csv --size 0

for i in {1..255}; do sudo arp -d 192.168.111.$i; done

for a in `seq 1 254`; do ping -c 1 -w 1 192.168.111.$a; done

date >> syussekilog.csv
arp -a >> syussekilog.csv
arp -a >> syusseki.csv