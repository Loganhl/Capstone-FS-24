import React,{useEffect,useState} from "react";
import axios from 'axios'
const Flagged = ()=>{
    const [flagged,setFlagged] = useState([]);
    useEffect(()=>{
        axios.get('http://backend:2500/api/flagged',{
            
        })
    })
}