import Keycloak from "keycloak-js";
import paths from '../paths.json'
const client = new Keycloak({

    "clientId":"frontend",
    "realm":"biovault",
    "url":"http://localhost:8080",
    credentials: {
        secret: 'wVECLGkzi5rQZoTWrDcEoxp3qhFGlN2T'
      }
})
export default client;
