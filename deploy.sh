#!/bin/bash
echo "config.py is not deployed"
#scp ~/workspace/WiFSIP/src/config.py sro@stella:/stella/home/sro/scripts/

scp ~/workspace/WiFSIP/src/nightshow.py sro@stella:/stella/home/sro/scripts/
scp ~/workspace/WiFSIP/src/obslog.py sro@stella:/stella/home/sro/scripts/
scp ~/workspace/WiFSIP/src/envlog.py sro@stella:/stella/home/sro/scripts/
scp ~/workspace/WiFSIP/src/gauge.py sro@stella:/stella/home/sro/scripts/
scp ~/workspace/WiFSIP/www/index.html sro@stella:/stella/home/sro/www/stella/graphs/
scp ~/workspace/WiFSIP/www/wifsip.html sro@stella:/stella/home/sro/www/stella/graphs/
