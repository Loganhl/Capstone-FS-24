import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Table } from 'react-bootstrap';

const DataTable = () => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:2500/api/users')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('There was an error fetching the data!', error);
      });
  }, []);

  return (
    <Table striped bordered hover>
      <thead>
        <tr>
          <th>Userid</th>
          <th>User</th>
          <th>Email</th>
          <th>First Name</th>
          <th>Last Name</th>
        </tr>
      </thead>
      <tbody>
        {data.map((item) => (
          <tr key={item.id}>
            <td>{item.ID}</td>
            <td>{item.USERNAME}</td>
            <td>{item.EMAIL}</td>
            <td>{item.FIRST_NAME}</td>
            <td>{item.LAST_NAME}</td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

export default DataTable;
