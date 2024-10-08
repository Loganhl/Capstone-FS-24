import logo from './logo.svg';
// import './App.css';
import { Button } from 'react-bootstrap';
import 'bootstrap/dist/css/bootstrap.css';
import React, { useEffect, useRef, useState } from 'react';
import ActiveUsers from './components/activeusers';
import getKeycloak from './components/kc';

function App() {
  const [authenticated, setAuthenticated] = useState(false);
  const didInit = useRef(false);
  const keycloak = getKeycloak();

  useEffect(() => {
    if (!didInit.current) {
      didInit.current = true;
      keycloak.init({ onLoad: 'login-required' }).then((authenticated) => {
        setAuthenticated(authenticated);
      }).catch((error) => {
        console.log("Error initializing Keycloak", error);
      });
    }
    
  }, []); // Corrected useEffect for Keycloak initialization
  if (!authenticated) {
    return <div>Loading...</div>;
  }
  return (
    <div className="App">
      <header className="App-header">
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        {/* <ActiveUsers /> */}
        <Button variant='dark' onClick={() => keycloak.logout()}>Grant</Button> {/* Corrected onClick handler */}
      </header>
    </div>
  );
}

export default App;
