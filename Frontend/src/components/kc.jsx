// import Keycloak from 'keycloak-js'

// const getKeycloak = new Keycloak({
//     "clientId":"biovault",
//     "realm":"biovault",
//     "url":"http://localhost:8080/"
// })
// // const getKeycloak = ()=>{
// //     let keycloakInstance = null;
// //     if (!keycloakInstance) {
// //         keycloakInstance = new Keycloak({
// //             "clientId":"biovault",
// //             "realm":"biovault",
// //             "url":"http://localhost:8080/",
// //         })
// //     }
// //     return keycloakInstance;
// // }
// export default getKeycloak;
import Keycloak from 'keycloak-js';

let keycloakInstance;

const getKeycloak = () => {
    if (!keycloakInstance) {
        keycloakInstance = new Keycloak({
            url: 'https://localhost:8443/',
            realm: 'BioVault',
            clientId: 'biovault',
        });
    }
    return keycloakInstance;
};

export default getKeycloak;
