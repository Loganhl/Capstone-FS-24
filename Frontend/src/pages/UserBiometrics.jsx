import React,{useEffect,useRef,useState} from "react";
import AvgDwellTime from "../components/Metrics/AvgDwell";
import WordsPerMin from "../components/Metrics/Wpm";
import { Row,Col,Container } from "react-bootstrap";
import MouseData from "../components/Metrics/MouseData";
const MyBiometrics = ({token,client})=>{
    return (<Container fluid>
        <Row>
            <Col>
                <AvgDwellTime token={token} client={client}></AvgDwellTime>
            </Col>
            <Col>
                <WordsPerMin token={token} client={client}></WordsPerMin>
            </Col>
        </Row>
        
    </Container>)
}

export default MyBiometrics;