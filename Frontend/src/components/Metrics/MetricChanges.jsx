import React from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2'
import {da, faker} from '@faker-js/faker'
const grant = [90,140,80,200,430,390,630,550,375,267]
export const options = {
  responsive: true,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  stacked: false,
  plugins: {
    title: {
      display: true,
      text: 'Chart.js Line Chart - Multi Axis',
    },
  },
  scales: {
    y: {
      type: 'linear',
      display: true,
      position: 'left',
    },
    y1: {
      type: 'linear',
      display: false,
      position: 'right' ,
      grid: {
        drawOnChartArea: false,
      },
    },
    y2: {
      type:'linear',
      display: false,
      // position:'center',
      grid:{
        drawOnChartArea:false,
      },
    },
  },
};
const labels = ['January', 'February', 'March', 'April', 'May', 'June', 'July','August','September','October','November'];

export const data = {
  labels,
  datasets: [
    {
      label: 'Logan',
      data: labels.map(() => faker.number.int({ min: -1000, max: 1000 })),
      borderColor: 'rgb(255, 99, 132)',
      backgroundColor: 'rgba(255, 99, 132, 0.5)',
      yAxisID: 'y',
    },
    {
      label: 'Grant',
      data: labels.map(() => faker.number.int({min:-1000,max:1000})),
      borderColor: 'rgb(53, 162, 235)',
      backgroundColor: 'rgba(53, 162, 235, 0.5)',
      yAxisID: 'y1',
    },
    {
      label:'Brendan',
      data: labels.map(()=> faker.number.int({min:-1000, max:1000})),
      borderColor: 'rgb(125,53,99)',
      backgroundColor:'rgba(125,53,99,0.5)',
      yAxisID:'y2'
    },
  ],
};

export function MetricChanges() {
  return <div> <Line height={90} options={options} data={data} /> </div>;
}