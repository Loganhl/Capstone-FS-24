import React from "react";
import { Container } from "react-bootstrap";
import {ReactComponent as Logo} from '../logo.svg';

const Home = ({ theme })=>{

    const backgroundColor = theme === "dark" ? "#343a40" : "darkgray";

    return(<div style={{display: 'flex',  justifyContent:'center', alignItems:'center', alignContent:"center", backgroundColor, height:600}}>
        <Container style={{textAlign: 'center'}}>
            <Logo style={{ width: '170px', height: '170px' }} />
            <h1>Welcome to Biovault</h1>
            <br />              
            <p>Here is where you can view metrics such as Words typed per minute and even average mouse dwell time!</p>
            <br />
            <p>You can also view Documentation for our project by clicking the link to our github page below in the footer!</p>
        </Container>        
    </div>)
}

export default Home;