import Keycloak from "keycloak-js";
import paths from '../paths.json'
const client = new Keycloak({
    "clientId":"frontend",
    "realm":"biovault",
    "url":"http://localhost:8080"
})
export default client;
