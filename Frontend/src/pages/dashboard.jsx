import React,{useState,useEffect,useRef} from "react";
import useAuth from "../hooks/useAuth";
import { MetricChanges } from "../components/Metrics/MetricChanges";
import ActiveUsers from "../components/activeusers";
import { Container,Row,Col } from "react-bootstrap";
const Dashboard = ({token,client})=>{
    return(
    <div>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
    <Container fluid='md'>
        <Container>
        <Row xs={1}>
            <MetricChanges/>
        </Row>
        <Row>
            <ActiveUsers token={token} client={client}></ActiveUsers>
        </Row>
        </Container>
    </Container>
    </div>)
}

export default Dashboard;