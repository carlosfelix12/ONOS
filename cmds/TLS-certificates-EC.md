
# Generate keystore in each machine

## Step-1 - EC
M1$ keytool -genkeypair -alias ONOS_EC -keyalg EC -sigalg SHA512withECDSA -validity 360 -keystore "./zKeystore/keystore_ECDSA" -ext SAN=dns:tls-onos-1,ip:10.3.1.203
M2$ keytool -genkeypair -alias ONOS_EC -keyalg EC -sigalg SHA512withECDSA -validity 360 -keystore "./zKeystore/keystore_ECDSA" -ext SAN=dns:tls-onos-2,ip:10.3.1.160

## Step-2 - Get certificate in P12 format

M1$ keytool -importkeystore -srckeystore ./zKeystore/keystore_ECDSA -destkeystore tls-onos-1.p12 -srcstoretype jks -deststoretype pkcs12
M2$ keytool -importkeystore -srckeystore ./zKeystore/keystore_ECDSA -destkeystore tls-onos-2.p12 -srcstoretype jks -deststoretype pkcs12


## Step-3 - Export from P12 format to PEM format

M1$ openssl pkcs12 -in tls-onos-1.p12 -out tls-onos-1.pem
M2$ openssl pkcs12 -in tls-onos-2.p12 -out tls-onos-2.pem

## Step-4 - Grab the certificate part of the pem to be shared with other hosts...

M1$ awk 'split_after == 1 {n++;split_after=0} /-----END ENCRYPTED PRIVATE KEY-----/ {split_after=1} {print > "cacert" n ".pem"}' < tls-onos-1.pem; mv cacert1.pem tls-onos-1-pub.pem
M2$ awk 'split_after == 1 {n++;split_after=0} /-----END ENCRYPTED PRIVATE KEY-----/ {split_after=1} {print > "cacert" n ".pem"}' < tls-onos-2.pem; mv cacert1.pem tls-onos-2-pub.pem

M1$ scp tls-onos-1-pub.pem admin@node2:
M2$ scp tls-onos-2-pub.pem admin@node1:

## Step 5 - Import certificates from other node

M1$ keytool -importcert -file tls-onos-2-pub.pem -keystore ./zKeystore/keystore_ECDSA
M2$ keytool -importcert -file tls-onos-1-pub.pem -keystore ./zKeystore/keystore_ECDSA

## Step 6 - Create dockers or copy current keystores to dockers.
Follow steps in TLS-onos-cluster-setup

