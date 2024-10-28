import { DoughnutController } from "chart.js";
import React from "react";
import {Doughnut} from 'react-chartjs-2'
const Keyspersec = ()=>{
  const  data = {
        labels: ['Brady Cook', 'Chase Daniel', 'Drew Lock', 'Brad Smith', 'Sam Horn', 'Blaine Gabbert'],
        datasets: [
          {
            label: 'Keys per Second',
            data: [12, 13, 7, 4, 4, 9],
            backgroundColor: [
              'rgba(255, 99, 132, 0.9)',
              'rgba(54, 162, 235, 0.7)',
              'rgba(255, 206, 86, 0.7)',
              'rgba(75, 192, 192, 0.7)',
              'rgba(153, 102, 255, 0.7)',
              'rgba(255, 159, 64, 0.7)',
            ],
            borderColor: [
              'rgba(255, 99, 132, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(255, 206, 86, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)',
              'rgba(255, 159, 64, 1)',
            ],
            borderWidth: 1,
          },
        ],
      };
      return(
        <Doughnut data={data}/>
      )
}
export default Keyspersec;