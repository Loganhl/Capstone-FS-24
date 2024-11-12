import React,{useState,useRef,useEffect} from "react";
import axios from 'axios';
import { Line } from "react-chartjs-2";
const WordsPerMin = ({token,client,userinfo})=>{
    const [wpm,setwpm] = useState([]);
    useEffect(()=>{
        axios.get('http://localhost:2500/api/wpm',{
            "headers":{
                "Authorization":`Bearer ${token}`,
            
            },
            "data":userinfo,
            'responseType':"json",
            "withXSRFToken":true
        }).then(res => setwpm(res.data)).catch(err=> console.log(err));
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
                text:'Words Per Minute',
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
    var labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
    var ds = {
        labels,
        datasets:[
            {
                label:'User',
                data: wpm.map((item)=>  item.value),
                borderColor: 'rgb(86,127,251)',
                backgroundColor: 'rgba(86,127,251,0.5)',
                yAxisID:'y',
            },
        ],
    }
    return(<div>
        <br></br>
        <br></br>
        <br></br>
        <Line height={90} options={options} data={ds}></Line>
    </div>)
}

export default WordsPerMin;