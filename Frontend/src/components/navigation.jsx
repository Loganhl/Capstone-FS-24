import React, { useEffect, useRef, useState } from "react";
import { Navbar, Nav, Container, Form } from "react-bootstrap";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "../pages/home";
import MyBiometrics from "../pages/UserBiometrics";
import Dashboard from "../pages/dashboard";
import {ReactComponent as Logo} from '../logo.svg';

const Navigation = ({ token, client, userinfo, theme, toggleTheme}) => {
  const navbarRef = useRef(null);
  const [isExpanded, setIsExpanded] = useState(false);

  const handleToggle = () => {
    setIsExpanded(!isExpanded);
  }

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (navbarRef.current && !navbarRef.current.contains(event.target)) {
        const navbarToggle = navbarRef.current.querySelector(".navbar-toggler");
        if (navbarToggle && navbarToggle.classList.contains("collapsed")) {
          return;
        }
        navbarToggle.click();
      }
    };

    document.addEventListener("click", handleClickOutside);

    return () => {
      document.removeEventListener("click", handleClickOutside);
    };
  })

  return (
    <Router>
      <Navbar
        ref = {navbarRef}
        position="sticky"
        expand="lg"
        className={`navbar-${theme} bg-body-${theme}`}
        variant={theme === "light" ? "light" : "dark"}
      >
        <Container>
          <Nav variant="tabs" defaultActiveKey="/">
            <div className="d-flex align-items-center">
              <Logo style={{ width: '50px', height: '50px' }} />
              <Navbar.Brand href="">Biovault</Navbar.Brand>
              <Navbar.Toggle onClick={handleToggle}>
                {isExpanded ? 'Collapse' : 'Expand'}
              </Navbar.Toggle>
            </div>
            <Navbar.Collapse id="navbar-nav">
              <Nav.Item>
                <Nav.Link as={Link} to="/">
                  Home
                </Nav.Link>
              </Nav.Item>
              {/* <Nav.Item>
                <Nav.Link as={Link} to="/biometrics">
                  My Biometrics
                </Nav.Link>
              </Nav.Item> */}
              {client.hasRealmRole &&
              <Nav.Item>
                <Nav.Link as={Link} to="/dashboard">
                  Admin Dashboard
                </Nav.Link>
              </Nav.Item>
              }
              <Nav.Item>
                <Nav.Link onClick={() => client.logout()}>Log out</Nav.Link>
              </Nav.Item>
              <Form.Check
                type="switch"
                id="theme-switch"
                label="Dark Mode"
                checked={theme === "dark"}
                onChange={toggleTheme}
                className="ms-3 custom-switch"
              />
            </Navbar.Collapse>
          </Nav>
        </Container>
      </Navbar>
      <Routes>
        <Route exact path="/" element={<Home />} />
        {/* <Route
          path="/biometrics"
          element={<MyBiometrics token={token} client={client} userinfo={userinfo}/>}
        /> */}
        <Route path="/dashboard" element={<Dashboard token={token} client={client} userinfo={userinfo} theme={theme}/>} />
      </Routes>
    </Router>
  );
};

export default Navigation;
