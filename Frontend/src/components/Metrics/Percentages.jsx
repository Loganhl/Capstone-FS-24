import React, { useEffect, useState } from "react";
import { Line } from "react-chartjs-2";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';

const Percentages = ({ token,userid,username }) => {
  const [metrics, setMetrics] = useState([]);
  const [data, setData] = useState([]);
  // userid = 'f08d8dfc-753f-47dc-9704-00a8a89b82ca'
  useEffect(() => {
    const fetchData = () => {
      const subscription = from(ajax({
        url: `${process.env.REACT_APP_API_URL}api/percentages/${userid}`,
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
    const interval = setInterval(fetchData, 60000); // Fetch new data every 60 seconds

    return () => clearInterval(interval); // Cleanup interval on unmount
  }, [token,userid]);

  useEffect(() => {
    if (metrics.length > 0) {
      setData(metrics);
    }
  }, [metrics]);

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      title: {
        display: true,
        text: `${username}'s Anomaly Percentages`,
        font: {
          size: 24
        },
        padding: 0
      },
      subtitle: {
        display: true,
        text: 'Refreshed Every Sixty Seconds',
        font: {
          size: 16
        },
        padding: 15
      },
    },
    scales: {
      y: {
        type: 'linear',
        display: true,
        position: 'left',
        title: {
          display: true,
          text: 'Percentage (%)'
        }
      },
      x: {
        display: true,
        title: {
          display: true,
          text: 'Time (Seconds)'
        }
      }
    },
    transitions: {
      show: {
        animations: {
          x: {
            from: 0
          },
          y: {
            from: 0
          }
        }
      },
      hide: {
        animations: {
          x: {
            from: 0
          },
          y: {
            from: 0
          }
        }
      },
    }
  };

  const labels = [5,10,15,20,25,30,35,40,45,50,55,60];
  const ds = {
    labels,
    datasets: [
      {
        label: `Average Time Between Keystrokes`,
        data: (data.length >0 ?data.map((item)=> item.avg_time_between_keystrokes_perc): []),
        borderColor: '#1b6d8c',
        backgroundColor:'#1b6d8cBF',
        spanGaps:true
      },
      {
        label: `Keys Per Second`,
        data: (data.length >0 ? data.map((item)=> item.keys_per_sec_perc): []),
        borderColor: '#227999',
        backgroundColor: '#227999BF',
        spanGaps:true,
      },
      {
        label: `Mouse Data`,
        data: (data.length >0 ? data.map((item)=> item.mouse_speed_perc): []),
        borderColor: '#2984A5',
        backgroundColor: '#2984A5BF',
        spanGaps: true,
      },
      {
        label:  `Words Per Minute`,
        data: (data.length > 0 ? data.map((item) => item.wpm_perc) : []),
        borderColor: '#399ABD',
        backgroundColor: '#399ABDBF',
        spanGaps:true,
        yAxisID: 'y',
      },
      {
        label:`Average Click Dwell Time`,
        data: (data.length >0 ? data.map((item)=> item.avg_click_dwell_perc) : []),
        borderColor: '#5BC6EE',
        backgroundColor:'#5BC6EEBF',
        spanGaps:true,
        yAxisID: 'y'
      },
      {
        label:`Average Dwell Time`,
        data:(data.length >0 ? data.map((item)=> item.avg_dwell_time_perc):[]),
        borderColor: '#84D8F8',
        backgroundColor: '#84D8F8BF',
        spanGaps:true,
        yAxisID:'y',
      }
    ],
  };

  return <Line data={ds} options={options}/>;
};

export default Percentages;
