import React,{useEffect,useState} from "react";
import axios from "axios";
//may have to move this function to the dashboard page.
//this function retrieves the username from the userid passed to it in the database. 
const GetUsernameFromID =  (token,userid)=>{
    const [username,setUsername] = useState('user');
    useEffect(()=>{
        axios.get(`${process.env.REACT_APP_API_URL}api/username/${userid}`,{
            "responseType":"text"
        }).then((resp)=>setUsername(resp.data));
        
    },[])
    return username;
}
export default GetUsernameFromID;