
# SBI certificates

RElevant sources: https://docs.openvswitch.org/en/latest/howto/ssl/
https://docs.pica8.com/display/PicOS21118sp/Configure+OVS+Connection+Using+SSL+with+Self-signed+Certificates 



# Step 1 - Create certificates for each switch (node with mininet)
ovs-pki init --force
cd /var/lib/openvswitch/pki/switchca

ovs-pki req+sign sc switch

Note: PKI files are stored in: /var/lib/openvswitch/pki




# Step 2 - create RSA certificate on ONOS

This assumes you have performed the steps in TLS-certificates-RSA file




# Step 3 - copy cacert.pem from ONOS

scp /home/admin/CROCUS/tls-onos-1-pub.pem admin@node_with_mininet:CROCUS/ovs-keys/

Note: do a backup of cacert.pem before.
mv /var/lib/openvswitch/pki/controllerca/cacert.pem /var/lib/openvswitch/pki/controllerca/bkp_cacert.pem

cp /home/admin/CROCUS/ovs-keys/tls-onos-1-pub.pem /var/lib/openvswitch/pki/controllerca/cacert.pem


# Step 4 - configure the use of cacert-onos.pem

ovs-vsctl set-ssl  /var/lib/openvswitch/pki/switchca/sc-privkey.pem  /var/lib/openvswitch/pki/switchca/sc-cert.pem  /var/lib/openvswitch/pki/controllerca/cacert.pem


# Step 5 - Copy certificate of switch to ONOS controller (from mininet node)

Copy "sc-cert.pem" (the OVS public key just generated in 2.1) to the ONOS host, 
scp /var/lib/openvswitch/pki/switchca/sc-cert.pem admin@node_with_onos:/home/admin/CROCUS/



 # Step 6 - import certificate
keytool -importcert -file sc-cert.pem -keystore zKeystore/keystore_RSA -alias switch-cert





11:43:51.323 INFO  [OFChannelInitializer] OpenFlow SSL enabled.
11:43:51.327 INFO  [OFChannelHandler] New switch connection from /10.3.2.82:40818
11:43:51.331 INFO  [OFChannelHandler] Switch disconnected callback for sw:[/10.3.2.82:40818 DPID[?]]. Cleaning up ...
11:43:51.335 WARN  [OFChannelHandler] no dpid in channelHandler registered for disconnected switch [/10.3.2.82:40818 DPID[?]]
11:43:51.347 DEBUG [SslHandler] [id: 0xbd1c63b2, L:/172.20.0.20:56974 - R:/172.20.0.10:5679] HANDSHAKEN: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
11:43:51.360 DEBUG [SslHandler] [id: 0xf2c719ca, L:/172.20.0.20:9876 - R:/172.20.0.21:49490] HANDSHAKEN: TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
11:43:51.367 TRACE [RemoteServerConnection] Received message type atomix-membership-probe from tls-onos2.onos:9876
11:43:51.371 TRACE [SwimMembershipProtocol] 172.20.0.20 - Received probe Member{id=172.20.0.20, address=172.20.0.20:9876, properties={state=ACTIVE, type=onos, version=2.2.2}, version=3.1.5, timestamp=1635417495228, state=ALIVE, incarnationNumber=1635417495229} from Member{id=172.20.0.21, address=172.20.0.21:9876, properties={state=READY, type=onos, version=2.2.2}, version=3.1.5, timestamp=1635415913964, state=ALIVE, incarnationNumber=1635415913967}



11:37:45.157 INFO  [OFChannelInitializer] OpenFlow SSL enabled.
11:37:45.161 INFO  [OFChannelHandler] New switch connection from /10.3.2.82:40810
11:37:45.162 INFO  [OFChannelHandler] Switch disconnected callback for sw:[/10.3.2.82:40810 DPID[?]]. Cleaning up ...
11:37:45.164 WARN  [OFChannelHandler] no dpid in channelHandler registered for disconnected switch [/10.3.2.82:40810 DPID[?]]
11:37:47.388 INFO  [OFChannelInitializer] OpenFlow SSL enabled.
11:37:47.390 INFO  [OFChannelHandler] New switch connection from /10.3.2.82:40814
11:37:47.480 INFO  [OFChannelInitializer] OpenFlow SSL enabled.
11:37:47.484 INFO  [OFChannelHandler] New switch connection from /10.3.2.82:40816
11:37:47.565 INFO  [OFChannelHandler] Sending OF_13 Hello to /10.3.2.82:40814
11:37:48.068 INFO  [OFChannelHandler] Sending OF_13 Hello to /10.3.2.82:40816
11:37:48.069 WARN  [OFChannelHandler] Config Reply from switch [/10.3.2.82:40814 DPID[00:00:00:00:00:00:00:01]] has miss length set to 128
11:37:48.074 INFO  [OFChannelHandler] Received meter features from [/10.3.2.82:40814 DPID[00:00:00:00:00:00:00:01]] with max meters: 4294967295
11:37:48.083 INFO  [OFChannelHandler] Received switch description reply OFDescStatsReplyVer13(xid=4294967289, flags=[], mfrDesc=Nicira, Inc., hwDesc=Open vSwitch, swDesc=2.13.3, serialNum=None, dpDesc=s1) from switch at /10.3.2.82:40814