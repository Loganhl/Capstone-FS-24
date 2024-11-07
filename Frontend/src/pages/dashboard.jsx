import React,{useState,useEffect,useRef} from "react";
import { MetricChanges } from "../components/Metrics/MetricChanges";

import { Container,Row,Col } from "react-bootstrap";
import Keysperec from '../components/Metrics/Keyspersec'

const Dashboard = ({token,client})=>{
    if (client.hasRealmRole('Admin') === false) {
        return( <div className="access-denied"> <br/><br/><br/><h1>ACCESS DENIED</h1> </div>)
    }
    
    
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