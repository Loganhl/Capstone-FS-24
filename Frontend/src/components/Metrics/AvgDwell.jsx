import React, { useEffect, useState } from "react";
import axios from 'axios';
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';
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
import paths from './../../paths.json'
import { it } from "@faker-js/faker";
import { Line } from "react-chartjs-2";

function convertResptoarray(array){
    for (let index = 0; index < array.length; index++) {
        const element = array[index];
        
    }
}
// const AvgDwellTime = ({token,client,userinfo})=>{
//     console.log(userinfo);
//     var [data,setData] = useState([])
//     useEffect(()=>{
//         axios.get(`http://localhost:2500/api/avgdwelltime`,{
//             'headers':{
//                 "Authorization":`Bearer ${token}`,
//             },
//             'responseType':'json',
//             'withXSRFToken':true,
//         }).then(resp=> setData(resp.data)).catch(err=> console.error(err));
//     },[])
//     var options = {
//         responsive: true,
//         interaction: {
//         mode: 'index',
//         intersect: false,
//     },
//     stacked:false,
//     plugins:{
//         title:{
//                 display:true,
//                 text:'Average Dwell Time',
//             },
//         },
//         scales:{
//             y:{
//                 type: 'linear',
//                 display:true,
//                 position:'left',
//             }
//         }
//     }
//     var labels = ['10 Seconds ago','20 Seconds ago','30 Seconds ago','40 Seconds ago','50 Seconds ago','60 Seconds ago']
//     var adataset = {
//         labels,
//         datasets:[
//             {
//                 label:'user',
//                 data:data.map((item)=> item.value),
//                 borderColor: 'rgb(53, 162, 235)',
//                 backgroundColor: 'rgba(53, 162, 235, 0.5)',
//                 yAxisID:'y',
//             },
//         ],
//     }
//     console.log(data.values())
//     return(
//     <div>
//         <br></br>
//         <br></br>
//         <br></br>
//         <Line height={90} options={options} data={adataset}></Line>
//     </div>
//     )

// }

// export default AvgDwellTime;



const AvgCDwellTime = ({ token, client, userinfo }) => {
  const [metrics, setMetrics] = useState([]);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      const subscription = from(ajax({
        url: `${process.env.REACT_APP_API_URL}api/avgdwelltime`,
        method: 'GET',
        headers: {
          "Authorization": `Bearer ${token}`,
        }
      })).pipe(
        map(response => response)
      ).subscribe({
        next: responseData => setMetrics(responseData.response || []),
        error: error => console.error('Error:', error),
        complete: () => console.log('Request complete')
      });
      return () => subscription.unsubscribe(); // Cleanup subscription on unmount
    };

    // Fetch data immediately
    fetchData();

    // Fetch data at intervals
    const interval = setInterval(fetchData, 5000); // Fetch new data every 5 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, [token]);

  useEffect(() => {
    if (metrics.length > 0) {
      setData(metrics);
    }
  }, [metrics]);

  const options = {
    responsive: true,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      title: {
        display: true,
        text: 'Average Dwell times Over the last 60 seconds',
      },
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
      },
    },
  };

  const labels = [10, 20, 30, 40, 50, 60];
  const ds = {
    labels,
    datasets: [
      {
        label: 'user',
        data: (data.length > 0 ? data.map((item) => item.value) : []),
        borderColor: 'rgb(86, 127, 51)',
        backgroundColor: 'rgba(86, 127, 51, 0.5)',
        yAxisID: 'y',
      },
    ],
  };

  return <Line data={ds} options={options} />;
};

export default AvgCDwellTime; 
