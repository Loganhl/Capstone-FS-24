import React, { useState, useEffect } from 'react';

const DataTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch('http://localhost:8000/api/anomalies/6242771f-785a-4c47-9c6a-6d5d8c8fffc6',
        {
            "mode":"cors"
        }
      )
      .then(data => setData(data))
      .catch(error => console.error('Error fetching data:', error));
      
  }, []);

  return (
    <table>
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Value</th>
        </tr>
      </thead>
      <tbody>
        {data && data.length > 0 ? (
          data.map(item => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>{item.email}</td>
              <td>{item.first_name}</td>
            </tr>
          ))
        ) : (
          <tr>
            <td colSpan="3">No data available</td>
          </tr>
        )}
      </tbody>
    </table>
  );
};

export default DataTable;
