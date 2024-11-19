import React,{useEffect,useState,useRef} from "react";
import axios from 'axios';
import { Line,Pie } from "react-chartjs-2";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';
// const MouseData = ({token,client}) =>{
//     const [data,setData] = useState([]);
//     useEffect(()=>{
//         axios.get('http://localhost:2500/api/mousespeed',{
//             "headers":{
//                 "Authorization":`Bearer ${token}`,
//             },
//             'withXSRFToken':true
//         }).then((res=> setData(res.data))).catch((err=> console.error(err)));
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
//                 text:'Mouse Data',
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
//     //needs to be changed
//     var labels = ['10 Seconds ago','20 Seconds ago','30 Seconds ago','40 Seconds ago','50 Seconds ago','60 Seconds ago'];
//     var adataset = {
//         labels,
//         datasets:[
//             {
//                 label:'user',
//                 data:data.map((item)=> item.value),
//                 borderColor: 'rgb(10, 205, 235)',
//                 backgroundColor: 'rgba(10, 205, 235, 0.5)',
//                 yAxisID:'y',
//             },
//         ],
//     }
//     return(
//         <div>
        
//             <Line options={options} data={adataset}></Line>
//         </div>
//     )
// }
const MouseData = ({ token, client, userid }) => {
    const [metrics, setMetrics] = useState([]);
    const [data, setData] = useState([]);
    userid = 'f08d8dfc-753f-47dc-9704-00a8a89b82ca'
    useEffect(() => {
      const fetchData = () => {
        const subscription = from(ajax({
          url: `${process.env.REACT_APP_API_URL}api/mousespeed/${userid}`,
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
    //GET NEWEST DATA TO APPEAR FIRST
    data.reverse()
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
          text: 'Mouse Speed',
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
  
    const labels = ['10 Seconds ago','20 Seconds ago','30 Seconds ago','40 Seconds ago','50 Seconds ago','60 Seconds ago'];
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
export default MouseData;