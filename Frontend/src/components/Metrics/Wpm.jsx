import React,{useState,useRef,useEffect} from "react";
import axios from 'axios';
import { Line } from "react-chartjs-2";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';

// const WordsPerMin = ({token,client,userinfo})=>{
//     const [wpm,setwpm] = useState([]);
//     useEffect(()=>{
//         axios.get('http://localhost:2500/api/wpm',{
//             "headers":{
//                 "Authorization":`Bearer ${token}`,
            
//             },
//             "data":userinfo,
//             'responseType':"json",
//             "withXSRFToken":true
//         }).then(res => setwpm(res.data)).catch(err=> console.log(err));
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
//                 text:'Words Per Minute',
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
//     var labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]
//     var ds = {
//         labels,
//         datasets:[
//             {
//                 label:'User',
//                 data: wpm.map((item)=>  item.value),
//                 borderColor: 'rgb(86,127,251)',
//                 backgroundColor: 'rgba(86,127,251,0.5)',
//                 yAxisID:'y',
//             },
//         ],
//     }
//     return(<div>
//         <br></br>
//         <br></br>
//         <br></br>
//         <Line height={90} options={options} data={ds}></Line>
//     </div>)
// }
const WordsPerMin = ({ token, client, userinfo }) => {
    const [metrics, setMetrics] = useState([]);
    const [data, setData] = useState([]);
  
    useEffect(() => {
      const fetchData = () => {
        const subscription = from(ajax({
          url: 'http://localhost:2500/api/wpm',
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
      const interval = setInterval(fetchData, 30000); // Fetch new data every 5 seconds
  
      return () => clearInterval(interval); // Cleanup interval on unmount
    }, [token]);
  
    useEffect(() => {
      if (metrics.length > 0) {
        setData(metrics);
      }
    }, [metrics]);
    //get newest data to appear first
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
          text: 'Words Per Minute',
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
  
    const labels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30];
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
export default WordsPerMin;