import React,{useState,useEffect,useRef} from "react";
import { MetricChanges } from "../components/Metrics/MetricChanges";

import { Container,Row,Col } from "react-bootstrap";
import Keysperec from '../components/Metrics/Keyspersec'
const Dashboard = ({token,client})=>{
    return(
    <div>
        <br></br>
        <br></br>
        <br></br>
    <Container fluid='md'>
        
        <Container>
        <br></br>    
        <Row xs={1} style={{height:400}}>
            <Col xs={10}>
                <MetricChanges/>
            </Col>
            <Col xs={3}>
                <Keysperec/>
            </Col>
        </Row>
        
        </Container>
    </Container>
    </div>)
}

export default Dashboard;