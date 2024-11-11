import React,{useEffect,useState} from "react";
import axios from 'axios';
import { Line } from "react-chartjs-2";
import { scales } from "chart.js";

const AvgClickDwell = ({token,client})=>{
    const [metrics,setmetrics] = useState([]);
    useEffect(()=>{
        axios.get('http://localhost:2500/clickdwelltime',{
            "headers":{
                "Authorization":`Bearer ${token}`,
            },
            "withXSRFToken":true,
        }).then((resp)=> setmetrics(resp.data)).catch((err=>console.error(err)));
    },[])
    var options = {
        responsive: true,
        interaction:{
            mode:'index',
            intersect:false,
        },
        stacked:false,
        plugins:{
            title:{
                display:true,
                text:"Average Click Dwelling Times",
            },
            scales:{
                y:{
                    type:'linear',
                    display:true,
                    position:'left',
                }
            }
        }
    }
    var labels = [10,20,30,40,50,60]
    var ds = {
        labels,
        datasets:[
            {
                label:'user',
                data:metrics.map((item)=> item.value),
                borderColor:'rgb(86,127,51)',
                backgroundColor:'rgba:(86,127,51,.05)',
                yAxisID:'y',
            }
        ]
    }
    return(<Line data={ds} options={options}></Line>)
}

export default AvgClickDwell;