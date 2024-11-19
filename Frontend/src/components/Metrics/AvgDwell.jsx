import React, { useEffect, useState } from "react";
import { from } from "rxjs";
import { map } from "rxjs/operators";
import { ajax } from 'rxjs/ajax';
import { Line } from "react-chartjs-2";

const AvgCDwellTime = ({ token, client, userid }) => {
  const [metrics, setMetrics] = useState([]);
  const [data, setData] = useState([]);

  useEffect(() => {
    const fetchData = () => {
      const subscription = from(ajax({
        url: `${process.env.REACT_APP_API_URL}api/avgdwelltime/${userid}`,
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
  }, [token, userid]); // Add userid as a dependency

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
        text: 'Average Dwell Times Over the Last 60 Seconds',
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
        label: 'User',
        data: data.length > 0 ? data.map(item => item.value) : [],
        borderColor: 'rgb(86, 127, 51)',
        backgroundColor: 'rgba(86, 127, 51, 0.5)',
        yAxisID: 'y',
      },
    ],
  };

  return (
    <div>
      <Line options={options} data={ds} />
    </div>
  );
};

export default AvgCDwellTime;