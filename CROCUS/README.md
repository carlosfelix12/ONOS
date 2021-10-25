# Ports used in ONOS and related services 
 830  - Netconf
 5678 - Atomix REST API
 5679 - Atomix intra-cluster communication
 6633 - OpenFlow legacy
 6640 - OVSDB
 6653 - OpenFlow IANA assigned
 8101 - ONOS CLI
 8181 - ONOS GUI
 9876 - ONOS intra-cluster communication

Verifications:
 - Traffic on 9876
 - Traffic on 5679
 - Traffic on 6653 


# TLS configuration
Configurations for TLS considering relevant information https://docs.oracle.com/en/java/javase/11/tools/keytool.html
Option -genkeypair ---> for key pair (public and privat keys pairs), thus suitable for RSA or DSA

## RSA
keytool -genkeypair -alias ONOS_RSA -keyalg RSA -keysize 2048 -sigalg SHA256withRSA -validity 360 -keystore "./keystore_RSA" -ext SAN=dns:onos-1,ip:10.3.3.219

with Is CN=onos-1, OU=dei, O=uc, L=coimbra, ST=coimbra, C=pt 

## DSA
keytool -genkeypair -alias ONOS_DSA -keyalg DSA -keysize 2048 -sigalg SHA256withDSA -validity 360 -keystore "./zKeystore/keystore_DSA" -ext SAN=dns:onos-1,ip:10.3.3.219

with Is CN=onos-1, OU=dei, O=uc, L=coimbra, ST=coimbra, C=pt 

## EC
keytool -genkeypair -alias ONOS_EC -keyalg EC -sigalg SHA512withECDSA -validity 360 -keystore "./zKeystore/keystore_ECDSA" -ext SAN=dns:onos-1,ip:10.3.3.219

with Is CN=onos-1, OU=dei, O=uc, L=coimbra, ST=coimbra, C=pt 

See the info here: https://docs.oracle.com/en/java/javase/11/security/oracle-providers.html#GUID-091BF58C-82AB-4C9C-850F-1660824D5254 



# Logging performance metrics
Possibilities:

## Jolokia (Not used)
1- use Jolokia as per https://karaf.apache.org/manual/latest/monitoring 
++ Allows to request in a curl basis the values of performance
++ Easy to activate feature
-- Requires knowledge regarding mbeans and overall metrics to gather values

## Decanter
2- Use decanter approach: as per http://karaf.apache.org/manual/decanter/latest-2/html/
-- Requires adding repo

### DO this: 
feature:repo-add decanter 2.8.0
feature:install decanter-collector-oshi   
feature:install decanter-collector-jetty
feature:install decanter-appender-file

### TLS Statistics
TLs statistics in Linux Kernel see info: https://www.kernel.org/doc/html/latest/networking/tls.html
/proc/net/tls_stat

Requirements:
apt-get install iproute2

After installing iproute2 one can use the tool 'ss'  with memory and in oneline output (https://man7.org/linux/man-pages/man8/ss.8.html)

ss -i -m --oneline

The following statistics may be provided:
    pacing_rate <pacing_rate>bps/<max_pacing_rate>bps the pacing rate and max pacing rate (transmission speed)
    delivery_rate: delivery rate n bps
    rtt:<rtt>/<rttvar> rtt is the average round trip time, rttvar is the mean deviation of rtt, their units are millisecond
    mss:<mss> max segment size
    cwnd:<cwnd> congestion window size
    pmtu:<pmtu> path MTU value
    bytes_received:<bytes_received> bytes received
    segs_out:<segs_out> segments sent out
    segs_in:<segs_in> segments received
    send <send_bps>bps egress bps

    ts     show string "ts" if the timestamp option is set
    sack   show string "sack" if the sack option is set
    ecn    show string "ecn" if the explicit congestion notification option is set
    ecnseen show string "ecnseen" if the saw ecn flag is found in received packets
    fastopen show string "fastopen" if the fastopen option is set
    cong_alg the congestion algorithm name, the default congestion algorithm is "cubic"
    wscale:<snd_wscale>:<rcv_wscale> if window scale option is used, this field shows the send scale factor and receive scale factor
    rto:<icsk_rto> tcp re-transmission timeout value, the unit is millisecond
    backoff:<icsk_backoff> used for exponential backoff re-transmission, the actual re-transmission timeout value is icsk_rto << icsk_backoff
    
    ato:<ato> ack timeout, unit is millisecond, used for delay ack mode
    ssthresh:<ssthresh> tcp congestion window slow start threshold bytes_acked:<bytes_acked> bytes acked
    
    lastsnd:<lastsnd> how long time since the last packet sent, the unit is millisecond
    lastrcv:<lastrcv> how long time since the last packet received, the unit is millisecond
    lastack:<lastack> how long time since the last ack received, the unit is millisecond
    
    
    

# SSH Configurations
Configure SSH to authorize keys
cat admin.pem.pub >> ~/.ssh/authorized_keys

Do a login wih the key to 
ssh -i admin.pem root@10.3.3.219
ssh -i admin.pem admin@10.3.3.219


# Mininet with TLS
https://wiki.onosproject.org/pages/viewpage.action?pageId=6358090

https://techandtrains.com/2014/04/27/open-vswitch-with-ssl-and-mininet/

sh ovs-vsctl set-controller s1 ssl:192.168.57.101:6653
sh ovs-vsctl set-controller s2 ssl:192.168.57.101:6653

