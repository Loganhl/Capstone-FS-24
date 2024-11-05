import React,{useEffect,useRef,useState} from "react";
import axios from "axios";
import { Table } from "react-bootstrap";
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    plugins,
    scales,
  } from 'chart.js';
import { it } from "@faker-js/faker";
import { Line } from "react-chartjs-2";

function convertResptoarray(array){
    for (let index = 0; index < array.length; index++) {
        const element = array[index];
        
    }
}
const AvgDwellTime = ({token,client})=>{
    var [data,setData] = useState([])
    useEffect(()=>{
        axios.get('http://localhost:2500/api/avgdwelltime',{
            'headers':{
                "Authorization":`Bearer ${token}`,
            },
            'responseType':'json',
            'withXSRFToken':true
        }).then(resp=> setData(resp.data)).catch(err=> console.error(err));
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
                text:'Average Dwell Time',
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
    var labels = ['10 Seconds ago','20 Seconds ago','30 Seconds ago','40 Seconds ago','50 Seconds ago','60 Seconds ago']
    var adataset = {
        labels,
        datasets:[
            {
                label:'user',
                data:data.map((item)=> item.value),
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
                yAxisID:'y',
            },
        ],
    }
    console.log(data.values())
    return(
    <div>
        <br></br>
        <br></br>
        <br></br>
        <Line height={90} options={options} data={adataset}></Line>
    </div>
    )

}

export default AvgDwellTime;