import React,{useEffect,useState,useRef} from "react";
import axios from 'axios';
import { Line,Pie } from "react-chartjs-2";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';

const BetweenStroke = ({ token, client, userinfo }) => {
    const [metrics, setMetrics] = useState([]);
    const [data, setData] = useState([]);
  
    useEffect(() => {
      const fetchData = () => {
        const subscription = from(ajax({
          url: 'http://localhost:2500/api/time_between_strokes',
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
    //GET THE NEWEST ENTRIES TO APPEAR FIRST
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
          text: 'Average Time between keystrokes Over the last 60 seconds',
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

  export default BetweenStroke;