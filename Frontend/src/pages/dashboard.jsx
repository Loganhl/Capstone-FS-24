import React, { useState, createContext, useRef, useEffect } from "react";
import axios from "axios";
import { Button, Col, Row, Table } from "react-bootstrap";
import AvgCDwellTime from "../components/Metrics/AvgDwell";
import AvgClickDwell from "../components/Metrics/AvgClickDwell";
const UserContext = createContext();

const RealmUsers = ({ token, setValue }) => {
  const [users, setUsers] = useState([]);
  const isRun = useRef(false);

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
      console.log(err);
    });
  }, [token]);
  const handlevaluechange = (newval) =>{
    setValue(newval);
    console.log(`user id should now be set to:${newval} `);
  }
  return (
    <Table>
      <tbody>
        {users.map((item) => (
          <tr key={item.ID}>
            <td>{item.username}</td>
            <td>{item.EMAIL}</td>
            <td>{item.FIRST_NAME}</td>
            <td>{item.LAST_NAME}</td>
            <td>
              <Button onClick={() => handlevaluechange(item.ID)}>View Metrics</Button>
            </td>
          </tr>
        ))}
      </tbody>
    </Table>
  );
};

const Dashboard = ({ token, client }) => {
  const [userid, setUserid] = useState('d7d75e80-39e6-4882-9b1b-e6e29dca1e70');

  if (!client.hasRealmRole("Admin")) {
    return <div>ACCESS DENIED</div>;
  }

  return (
    <div>
        <Row>
          <Col>
              <AvgCDwellTime token={token} userid={userid} />
          </Col>
          <Col>
            <AvgClickDwell token={token} userid={userid}/>
          </Col>
        </Row>
        <Row>
          <Col>

          </Col>
        </Row>
        <Row>
          <RealmUsers token={token} setValue={setUserid} />
        </Row>
      
    </div>
  );
};

export default Dashboard;