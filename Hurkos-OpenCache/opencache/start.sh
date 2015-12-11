#!/bin/bash

RED='\e[31m'
NC='\e[0m'

#Adatbázis inicializálása
sudo rm /var/lib/mongodb/mongod.lock
sudo mongod --repair -f /etc/mongod.conf
sudo mongod -f /etc/mongod.conf&

echo Javítás kész
clear

#route bejegyzések inicializálása
sudo ip route del 192.168.0.0/24 dev eth2

echo -e ${RED}OVS indítása...${NC}
#kernel space OVS indítása
sudo ovsdb-server --remote=punix:/usr/local/var/run/openvswitch/db.sock \
                    --remote=db:Open_vSwitch,Open_vSwitch,manager_options \
                    --private-key=db:Open_vSwitch,SSL,private_key \
                    --certificate=db:Open_vSwitch,SSL,certificate \
                    --bootstrap-ca-cert=db:Open_vSwitch,SSL,ca_cert \
                    --pidfile --detach

sudo ovs-vswitchd --pidfile --detach
sleep 2


#Floodligth controller indítása
echo -e ${RED}Floodlight-0.91 indítása...${NC}
#sudo gnome-terminal -e "sudo java -jar /home/sdn-tmit/floodlight-0.91/target/floodlight.jar 2>&1 | tee oc-log/fl-log.log"&
sudo gnome-terminal -e "sudo java -jar /home/sdn-tmit/floodlight-0.91/target/floodlight.jar"&
sleep 10

#OCC indítása
echo -e ${RED}OCC indítása...${NC}
sudo gnome-terminal -e "sudo opencache -c --config=/home/sdn-tmit/opencache/examples/config/controller.conf 2>&1 | tee oc-log/occ-log.log"&
sleep 3

#OCN indítása
echo -e ${RED}OCN indítása...${NC}
sudo gnome-terminal -e "sudo opencache -n --config=/home/sdn-tmit/opencache/examples/config/node.conf 2>&1 | tee oc-log/ocn-log.log"&
sleep 3

#OC-Console indítása
echo -e ${RED}OC-Console indítása...${NC}
sudo gnome-terminal -e "sudo python /home/sdn-tmit/opencache-console/console/console.py 2>&1 | tee oc-log/gui-log.log"

echo -e ${RED}OpenCache rendszer elindult${NC}



