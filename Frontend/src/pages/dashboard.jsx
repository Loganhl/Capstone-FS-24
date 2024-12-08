import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import { Card, Button, Col, Row, Table } from "react-bootstrap";
import AvgCDwellTime from "../components/Metrics/AvgDwell";
import AvgClickDwell from "../components/Metrics/AvgClickDwell";
import MouseData from "../components/Metrics/MouseData";
import WordsPerMin from "../components/Metrics/Wpm";
import BetweenStroke from "../components/Metrics/BetweenStroke";
import Percentages from "../components/Metrics/Percentages";

const RealmUsers = ({ token, setValue,setUsername,theme }) => {
  const [users, setUsers] = useState([]);
  const isRun = useRef(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (isRun.current) return;
    isRun.current = true;

    axios.get(`${process.env.REACT_APP_API_URL}api/users`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    .then((resp) => setUsers(resp.data))
    .catch((err) => {
      setError('Failed to fetch users. Please try again later.');
      console.error(err);
    });
  }, [token]);
  const handlevaluechange = (newval,newusername) =>{
    setValue(newval);
    setUsername(newusername);
    console.log(`user id should now be set to:${newval} `);
    console.log(`Username should now be ${newusername}`);
  }
  return (
    <div
    className="scrollable-container"
    style={{
      display: 'flex',
      flexDirection: 'column',
      maxHeight: 'calc(100vh - 250px)',
      overflowY: 'auto',
    }}
  >
    <Table variant={theme} striped hover>
        <thead style={{
          position: 'sticky',
          top: 0,
          zIndex: 2
        }}>
        <tr>
          <th>Username</th>
          <th>Email</th>
          <th>First</th>
          <th>Last</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {users.map((item) => (
          <tr key={item.ID}>
            <td>{item.username}</td>
            <td>{item.EMAIL}</td>
            <td>{item.FIRST_NAME}</td>
            <td>{item.LAST_NAME}</td>
            <td>
              <Button
                  onClick={() => handlevaluechange(item.ID,item.username)}
                  style={{ backgroundColor: '#227999', borderColor: '#1B6D8C'}}
              >View Metrics</Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
    </div>
    )}

const Dashboard = ({ token, client,theme }) => {
  const [userid, setUserid] = useState('45b5ad85-3d4e-4389-8bf5-70ca75f2f210');
  const [username,setUsername] = useState('kaelyn');

  if (!client.hasRealmRole("Admin")) {
    return <div>ACCESS DENIED</div>;
  }
  const getCardStyle = (theme) => ({
    backgroundColor: theme === "dark" ? "#343a40" : "#f8f9fa",
    color: theme === "dark" ? "#ffffff" : "#212529",
    borderColor: theme === "dark" ? "#495057" : "#dee2e6",
  });

  return (
    <div className="dashboard-container" style={{display: 'flex', flexDirection: 'column', height: '85vh' }}>
      <Row className="g-3" style={{ flex: 1 }}>
        <Col md={4} style={{ display: 'flex', flexDirection: 'column' }}>
          <Card style={getCardStyle(theme)} className="flex-grow-1">
            <Card.Body className="d-flex flex-column">
              <Card.Title className="text-center">User Management</Card.Title>
              <RealmUsers
                token={token}
                setValue={setUserid}
                setUsername={setUsername}
                theme={theme}
              />
            </Card.Body>
          </Card>
        </Col>

        <Col md={8} style={{ display: 'flex', flexDirection: 'column' }}>
          <Card style={getCardStyle(theme)} className="flex-grow-1">
            <Card.Body className="d-flex flex-column">
              <Percentages token={token} userid={userid} username={username} hieght={500}/>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;