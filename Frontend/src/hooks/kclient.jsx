import Keycloak from "keycloak-js";
import paths from '../paths.json'
const client = new Keycloak({
    "clientId":paths.keycloakclient_id,
    "realm":paths.keycloak_realm,
    "url":paths.keycloakurl
})
export default client;
