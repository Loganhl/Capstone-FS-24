import React,{useState,useEffect,useRef} from "react";
import useAuth from "../hooks/useAuth";
import { MetricChanges } from "../components/Metrics/MetricChanges";
import ActiveUsers from "../components/activeusers";
import { Container,Row,Col } from "react-bootstrap";
import Keysperec from '../components/Metrics/Keyspersec'
const Dashboard = ({token,client})=>{
    return(
    <div>
        <br></br>
        <br></br>
        <br></br>
        <br></br>
    <Container fluid='md'>
        <Container>
        <Row xs={1} style={{height:400}}>
            <MetricChanges/>
        </Row>
        <Row xs={1} style={{height:400}}>
            <Keysperec/>
        </Row>
        <Row>
            <ActiveUsers token={token} client={client}></ActiveUsers>
        </Row>
        </Container>
    </Container>
    </div>)
}

export default Dashboard;