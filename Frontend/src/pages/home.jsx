import React,{useRef,useState,useEffect} from "react";
import { Container } from "react-bootstrap";


const Home = ()=>{
    return(<div style={{alignContent:"center", backgroundColor:"darkgray",height:600}}>
        <Container>
            <h1>Welcome to Biovault</h1>
            <p>Here is where you can view metrics such as Words typed per minute and even average mouse dwell time!</p>
            <br></br>
            <p>You can also view Documentation for our project by clicking the link to our github page below in the footer!</p>
        </Container>        
    </div>)
}

export default Home;