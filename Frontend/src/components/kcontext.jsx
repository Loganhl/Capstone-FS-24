import React, { createContext, useContext, useEffect, useState } from 'react';
import getKeycloak from './keycloak';
import adapter from './adapter.json'

const KeycloakContext = createContext(null);

export const KeycloakProvider = ({ children }) => {
    const [keycloak, setKeycloak] = useState(getKeycloak());

    useEffect(() => {
        keycloak.init({ onLoad: 'login-required'  }).catch(console.error);
    }, [keycloak]);

    return (
        <KeycloakContext.Provider value={keycloak}>
            {children}
        </KeycloakContext.Provider>
    );
};

export const useKeycloak = () => useContext(KeycloakContext);
