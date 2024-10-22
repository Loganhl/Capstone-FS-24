FROM quay.io/keycloak/keycloak:26.0.0 as builder
#import the biovault-realm to the data import folder
COPY  ./biovault-realm.json /opt/keycloak/data/import

WORKDIR /opt/keycloak

#run the realm import operation
RUN /opt/keycloak/bin/kc.sh build
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:keycloak,IP:127.0.0.1" -keystore conf/server.keystore
#finish the multistage build

FROM quay.io/keycloak/keycloak:latest
COPY --from=builder /opt/keycloak/ /opt/keycloak/

ENV KC_DB=mysql
ENV KC_DB_PASSWORD=secretsquirrels
ENV KC_DB_URL=jdbc:mysql://mysql:3306/biometric_auth
ENV KC_DB_USERNAME=root
ENV KC_BOOTSTRAP_ADMIN_PASSWORD=admin
ENV KC_BOOTSTRAP_ADMIN_USERNAME=admin
ONBUILD RUN /opt/keycloak/bin/kc.sh import --file /opt/keycloak/data/import/biovault-realm.json
ENTRYPOINT [ "/opt/keycloak/bin/kc.sh" ]