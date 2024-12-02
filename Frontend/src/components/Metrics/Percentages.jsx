import React, { useEffect, useState } from "react";
import axios from 'axios';
import { Line } from "react-chartjs-2";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';
import paths from '../../paths.json'
import { useTheme } from '../../hooks/ThemeProvider';
const Percentages = ({ token, client, userid,username }) => {
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
    interaction: {
      mode: 'index',
      intersect: false,
    },
    stacked: false,
    plugins: {
      title: {
        display: true,
        text: 'Anomaly Percantes refreshed every sixty seconds',
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

  const labels = [1, 2, 3, 4, 5, 6,7,8,9,10,11,12];
  const ds = {
    labels,
    datasets: [
      {
        label:  `${username} wpm_perc`,
        data: (data.length > 0 ? data.map((item) => item.wpm_perc) : []),
        borderColor: 'rgb(86, 127, 51)',
        backgroundColor: 'rgba(86, 127, 51, 0.5)',
        spanGaps:true,
        yAxisID: 'y',
      },
      {
        label:`${username} avg_click_dwell_perc`,
        data: (data.length >0 ? data.map((item)=> item.avg_click_dwell_perc) : []),
        borderColor: 'rgb(145, 220,95)',
        backgroundColor:'rgba(145, 220,95,0.5)',
        spanGaps:true,
        yAxisID: 'y'
      },
      {
        label:`${username} avg_dwell_time_perc`,
        data:(data.length >0 ? data.map((item)=> item.avg_dwell_time_perc):[]),
        borderColor: 'rgb(129,45,201)',
        backgroundColor: 'rgba(129,45,201,0.5)',
        spanGaps:true,
        yAxisID:'y',
      }
    ],
  };

  return <Line data={ds} options={options} />;
};

export default Percentages;
