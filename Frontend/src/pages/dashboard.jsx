import React from "react";
import { MetricChanges } from "../components/Metrics/MetricChanges";
import SelectUser from "../components/users";
import { Container, Row, Col } from "react-bootstrap";
import Keysperec from "../components/Metrics/Keyspersec";

const Dashboard = ({ token, client,userid }) => {
  if (client.hasRealmRole("Admin") === false) {
    return (
      <div className="access-denied">
        <h1 style={{textAlign: "center", marginTop: "100px"}}>ACCESS DENIED</h1>
      </div>
    );
  }

  return (
    <div>
      <Container fluid="md">
        <Container>
          <br></br>
          {/* <Row xs={1} style={{ height: 400 }}>
            <Col xs={10}>
              <MetricChanges />
            </Col>
            <Col xs={3}>
              <Keysperec />
            </Col>
          </Row> */}
            <SelectUser token={token} client={client}></SelectUser>
          <Row>
            
          </Row>
        </Container>
      </Container>
    </div>
  );
};

export default Dashboard;
