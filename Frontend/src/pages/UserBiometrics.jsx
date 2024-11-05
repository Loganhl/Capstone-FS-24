import React,{useEffect,useRef,useState} from "react";
import AvgDwellTime from "../components/Metrics/AvgDwell";


const MyBiometrics = ({token,client})=>{
    return <AvgDwellTime token={token}client={client} ></AvgDwellTime>
}

export default MyBiometrics;