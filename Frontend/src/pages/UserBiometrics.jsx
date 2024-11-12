import React from "react";
import AvgDwellTime from "../components/Metrics/AvgDwell";
import WordsPerMin from "../components/Metrics/Wpm";
import { Row,Col,Container } from "react-bootstrap";
import MouseData from "../components/Metrics/MouseData";
import AvgClickDwell from "../components/Metrics/AvgClickDwell";
const MyBiometrics = ({token,client,userinfo})=>{
    return (<Container fluid>
        <Row>
            <Col>
                <AvgDwellTime token={token} client={client} userinfo={userinfo}> </AvgDwellTime>
            </Col>
            <Col>
                <AvgClickDwell token={token} client={client} userinfo={userinfo}></AvgClickDwell>            
            </Col>
        </Row>
        <Row>
            <Col>
                <MouseData token={token} client={client} userinfo={userinfo}></MouseData>
            </Col>
            <Col>
                <WordsPerMin token={token} client={client} userinfo={userinfo}></WordsPerMin>
            </Col>
        </Row>
        
    </Container>)
}

export default MyBiometrics;