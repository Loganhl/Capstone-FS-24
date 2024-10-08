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
// const kc = new Keycloak({
//     "clientId":'biovault',
//     'realm':'biovault',
//     'url':"http://localhost:80"
// })

let keycloakInstance;


const getKeycloak = () => {
    if (!keycloakInstance) {
        keycloakInstance = new Keycloak({
            url: 'http://localhost/',
            realm: 'BioVault',
            clientId: 'biovault',
        });
    }
    return keycloakInstance;
};

export default getKeycloak;
