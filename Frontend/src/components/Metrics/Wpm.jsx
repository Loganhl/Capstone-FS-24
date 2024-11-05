import React,{useState,useRef,useEffect} from "react";
import axios from 'axios';

const WordsPerMin = ({token,client})=>{
    const [wpm,setwpm] = useState([]);
    useEffect(()=>{
        axios.get('http://localhost:2500/api/wpm',{
            "headers":{
                "Authorization":`Bearer ${token}`,
            },
            'responseType':"json"
        }).then(res => setwpm(res.data)).catch(err=> console.log(err));
    },[])
}