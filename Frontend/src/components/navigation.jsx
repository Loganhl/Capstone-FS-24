import React from "react";
import client from "../hooks/kclient";
import { Button,Navbar,Nav } from "react-bootstrap";

const Navigation = ({token})=>{
    return(<Navbar>
        <Navbar.Brand></Navbar.Brand>
        <Button variant="dark" onClick={()=> client.logout()}>Logout</Button>
        </Navbar>)
}

export default Navigation;