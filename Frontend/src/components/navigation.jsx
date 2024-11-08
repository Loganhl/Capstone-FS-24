import React, { useState, useEffect } from "react";
import { Navbar, Nav, Container, Form } from "react-bootstrap";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "../pages/home";
import MyBiometrics from "../pages/UserBiometrics";
import Dashboard from "../pages/dashboard";

const Navigation = ({ token, client, theme, toggleTheme }) => {
  return (
    <Router>
      <Navbar
        position="sticky"
        expand="lg"
        className={`navbar-${theme} bg-body-${theme}`}
        variant={theme === "light" ? "light" : "dark"}
      >
        <Container>
          <Nav variant="tabs" defaultActiveKey="/">
            <div className="d-flex align-items-center">
              <Navbar.Brand href="">Biovault</Navbar.Brand>
              <Navbar.Toggle aria-controls="navbar-nav">Collapse</Navbar.Toggle>
            </div>
            <Navbar.Collapse id="navbar-nav">
              <Nav.Item>
                <Nav.Link as={Link} to="/">
                  Home
                </Nav.Link>
              </Nav.Item>
              <Nav.Item>
                <Nav.Link as={Link} to="/biometrics">
                  My Biometrics
                </Nav.Link>
              </Nav.Item>
              
              <Nav.Item>
                <Nav.Link as={Link} to="/dashboard">
                  Admin Dashboard
                </Nav.Link>
              </Nav.Item>
              
              <Nav.Item>
                <Nav.Link onClick={() => client.logout()}>Log out</Nav.Link>
              </Nav.Item>
              <Form.Check
                type="switch"
                id="theme-switch"
                label="Dark Mode"
                checked={theme === "dark"}
                onChange={toggleTheme}
                className="ms-3"
              />
            </Navbar.Collapse>
          </Nav>
        </Container>
      </Navbar>
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route
          path="/biometrics"
          element={<MyBiometrics token={token} client={client} />}
        />
        <Route path="/dashboard" element={<Dashboard token={token} client={client} />} />
      </Routes>
    </Router>
  );
};

export default Navigation;
