import React,{useEffect,useState,useRef} from "react";
import axios from 'axios';
import { Line,Pie } from "react-chartjs-2";

const MouseData = ({token,client}) =>{
    const [data,setData] = useState([]);
    useEffect(()=>{
        axios.get('http://localhost:2500/api/mousespeed',{
            "headers":{
                "Authorization":`Bearer ${token}`,
            },
            'withXSRFToken':true
        }).then((res=> setData(res.data))).catch((err=> console.error(err)));
    },[])
    var options = {
        responsive: true,
        interaction: {
        mode: 'index',
        intersect: false,
    },
    stacked:false,
    plugins:{
        title:{
                display:true,
                text:'Mouse Data',
            },
        },
        scales:{
            y:{
                type: 'linear',
                display:true,
                position:'left',
            }
        }
    }
    //needs to be changed
    var labels = ['10 Seconds ago','20 Seconds ago','30 Seconds ago','40 Seconds ago','50 Seconds ago','60 Seconds ago'];
    var adataset = {
        labels,
        datasets:[
            {
                label:'user',
                data:data.map((item)=> item.value),
                borderColor: 'rgb(10, 205, 235)',
                backgroundColor: 'rgba(10, 205, 235, 0.5)',
                yAxisID:'y',
            },
        ],
    }
    return(
        <div>
        
            <Line options={options} data={adataset}></Line>
        </div>
    )
}

export default MouseData;