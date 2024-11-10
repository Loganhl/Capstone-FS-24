import React,{useEffect,useState} from "react";
import axios from 'axios';
import { Line } from "react-chartjs-2";
//need to decide whether or not we are going with a line graph for this.
const Percentages = ({token,client})=>{
    const [percent,setpercent] = useState([]);
    useEffect(()=>{
        axios.get('http://localhost:2500/api/percentages',{
            "headers":{
                "Authorization":`Bearer ${token}`,
            },
            "responseType":"json",
            "withXSRFToken":true,
        }).then((res)=> setpercent(res.data)).catch((err => console.error(err)));
    },[])
    
}

export default Percentages