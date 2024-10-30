import React,{useRef,useState,useEffect} from "react";
import {Button,Card,Container,Form,Carousel,ProgressBar} from 'react-bootstrap'
import useAuth from "../hooks/useAuth";
const Home = ({token,client})=>{
    return(<div style={{alignContent:"center", backgroundColor:"darkgray",height:600}}>
        <ProgressBar animated striped variant="success" min={15} now={20} max={100} ></ProgressBar>
    </div>)
}

export default Home;