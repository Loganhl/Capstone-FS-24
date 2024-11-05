import React from "react";
import { Button,Navbar,Nav, Container } from "react-bootstrap";
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Home from "../pages/home";
import MyBiometrics from "../pages/UserBiometrics";
import Dashboard from "../pages/dashboard";
import Login from "../pages/login";

const Navigation = ({token,client})=>{

    return(
    <Router>
        <Navbar  fixed="top" expand='lg' className="bg-body-tertiary">
            <Container>

            <Nav variant="tabs" defaultActiveKey='/'>
                <Navbar.Brand href="">Biovault</Navbar.Brand>
                <Nav.Item>
                    <Nav.Link as={Link} to='/'>Home</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link as={Link} to='/biometrics'>My Biometrics</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link as={Link} to='/dashboard'>Admin Dashboard</Nav.Link>
                </Nav.Item>
                <Nav.Item>
                    <Nav.Link onClick={()=> client.logout()}>Log out</Nav.Link>
                </Nav.Item>
                <Navbar.Toggle >Light</Navbar.Toggle>
            </Nav>
            </Container>
            </Navbar>
            <Routes>
                <Route exact path="/"  element={<Home/>}/>
                <Route path="/biometrics" element={<MyBiometrics token={token} client={client} />}/>
                <Route path="/dashboard" element={<Dashboard/>}/>
                
            </Routes>
        </Router>
        )
}

export default Navigation;