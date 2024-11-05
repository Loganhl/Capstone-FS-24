const Keycloak = require("keycloak-connect");
const dotenv = require('dotenv').config();
// const config = require("../keycloak.json")
//keycloak configuration variables so that tha backend connects with keycloak and secures the api.
const config = {
  "realm": process.env.KEYCLOAK_REALM,
  "auth-server-url": `${process.env.KEYCLOAK_URL}`,
  "ssl-required": "external",
  "resource": process.env.KEYCLOAK_CLIENT,
  "bearer-only": true,
  "credentials": {
    "secret": process.env.KEYCLOAK_CLIENT_SECRET
  },
}


module.exports = new Keycloak({}, config);