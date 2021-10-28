1. Docker Swarm SETUP

Two machines: M1 (.219) M2(.220)

M1$ docker swarm init

This will start the swarm (copy the instruction for docker swarm join)

M2$ docker swarm join .....



2. ONOS CLUSTER SETUP

M1$ docker network create -d overlay --attachable onos --subnet 172.20.0.0/16 --gateway 172.20.0.1

M1$ docker create -t -p 5679:5679 --restart unless-stopped --name tls-atomix-1 --hostname tls-atomix-1 --net onos --ip 172.20.0.10 atomix/atomix:3.1.5
M2$ docker create -t -p 5679:5679 --restart unless-stopped --name tls-atomix-2 --hostname tls-atomix-2 --net onos --ip 172.20.0.11 atomix/atomix:3.1.5

export OC1=172.20.0.10
export OC2=172.20.0.11

cd ~
M1$ ./onos/tools/test/bin/atomix-gen-config 172.20.0.10 Documents/onos-config-files/tls-atomix-1.conf 172.20.0.10 172.20.0.11
M2$ ./onos/tools/test/bin/atomix-gen-config 172.20.0.11 Documents/onos-config-files/tls-atomix-2.conf 172.20.0.10 172.20.0.11

cd CROCUS
M1$ docker cp ./zKeystore/keystore_RSA tls-atomix-1:/opt/atomix/conf/keystore
M2$ docker cp ./zKeystore/keystore_RSA tls-atomix-2:/opt/atomix/conf/keystore

Edit atomix configuration to include 'cluster.messaging.tls' Remember to have a valid JSON file
    cluster.messaging.tls:
    {
        enabled: true
        keyStore: /opt/atomix/conf/keystore
        keyStorePassword: <The Password you have defined>
        trustStore: /opt/atomix/conf/keystore
        trustStorePassword: <The Password you have defined>
    }


M1$ docker cp Documents/onos-config-files/tls-atomix-1.conf tls-atomix-1:/opt/atomix/conf/atomix.conf
M2$ docker cp Documents/onos-config-files/tls-atomix-2.conf tls-atomix-2:/opt/atomix/conf/atomix.conf

M1$ docker container start tls-atomix-1
M21$ docker container start tls-atomix-2

ALL$ add the option  -DenableNettyTLS=true  to JAVA_OPTS in bin/atomix-agent script inside each tls-atomix container


M1$ docker run -t -d -p 80:8181 -p 443:8443  -p 8101:8101 -p 6653:6653 -p 6633:6633 -p 5005:5005 -p 830:830 --restart unless-stopped --name tls-onos1 --hostname tls-onos1 --net onos --ip 172.20.0.20 -e ONOS_APPS="drivers,openflow,lldpprovider,proxyarp,fwd,gui2" onosproject/onos:2.2.2
M2$ docker run -t -d -p 80:8181 -p 443:8443 -p 8101:8101 -p 6653:6653 -p 6633:6633 -p 5005:5005 -p 830:830 --restart unless-stopped --name tls-onos2 --hostname tls-onos2 --net onos --ip 172.20.0.21 -e ONOS_APPS="drivers,openflow,lldpprovider,proxyarp,fwd,gui2" onosproject/onos:2.2.2

M1$ ./onos/tools/test/bin/onos-gen-config 172.20.0.20 Documents/onos-config-files/tls-cluster-1.json -n 172.20.0.10 172.20.0.11
M2$ ./onos/tools/test/bin/onos-gen-config 172.20.0.21 Documents/onos-config-files/tls-cluster-2.json -n 172.20.0.10 172.20.0.11

M1$ docker exec tls-onos1 mkdir /root/onos/config
M2$ docker exec tls-onos2 mkdir /root/onos/config

M1$ docker cp Documents/onos-config-files/tls-cluster-1.json tls-onos1:/root/onos/config/cluster.json
M2$ docker cp Documents/onos-config-files/tls-cluster-2.json tls-onos2:/root/onos/config/cluster.json

cd CROCUS
M1$ docker cp ./zKeystore/keystore_RSA tls-onos1:/root/onos/apache-karaf-4.2.8/etc/keystore
M2$ docker cp ./zKeystore/keystore_RSA tls-onos2:/root/onos/apache-karaf-4.2.8/etc/keystore

Enter in the docker to change the start configuration and add the following content On the first lines of the file bin/onos-service:

   export JAVA_OPTS="${JAVA_OPTS:--Dio.atomix.enableNettyTLS=true -DenableOFTLS=true -Djavax.net.ssl.keyStore=/root/onos/apache-karaf-4.2.8/etc/keystore -Djavax.net.ssl.keyStorePassword=crocustls -Djavax.net.ssl.trustStore=/root/onos/apache-karaf-4.2.8/etc/keystore -Djavax.net.ssl.trustStorePassword=crocustls}"

Inside docker confirm keys in the keystore:

keytool -list -keystore /root/onos/apache-karaf-4.2.8/etc/keystore

    Enter keystore password:  
    Keystore type: PKCS12
    Keystore provider: SUN

    Your keystore contains 3 entries

    mykey, Oct 28, 2021, trustedCertEntry, 
    Certificate fingerprint (SHA-256): F1:51:9A:F5:14:DA:BC:D6:7E:7E:0E:03:A6:D2:3A:BE:68:5E:90:F4:56:99:58:6B:17:10:EC:CC:C4:3B:CF:D2
    onos_rsa, Oct 28, 2021, PrivateKeyEntry, 
    Certificate fingerprint (SHA-256): 74:35:88:FD:CC:2D:51:A0:3F:0C:FC:30:B7:42:A8:98:21:A2:EC:4F:97:9A:9C:AF:C3:BC:50:F4:A5:6B:44:B5
    switch-cert, Oct 28, 2021, trustedCertEntry, 
    Certificate fingerprint (SHA-256): E6:DF:8E:C1:5F:FB:5E:AC:64:33:1C:29:20:14:90:89:25:5C:1C:68:67:BE:BA:79:91:6E:AD:AF:A2:13:72:70


# Step xx - Edit the configuration of org.ops4j.pax.web.cfg 

vim /root/onos/apache-karaf-4.2.8/etc/org.ops4j.pax.web.cfg 

    org.osgi.service.http.secure.enabled=true
    org.ops4j.pax.web.ssl.keystore=etc/keystore
    org.ops4j.pax.web.ssl.password=crocustls
    org.ops4j.pax.web.ssl.keypassword=crocustls


M1$ docker restart tls-onos1
M2$ docker restart tls-onos2