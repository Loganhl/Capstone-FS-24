import React,{useState,useEffect,useRef} from "react";
import axios from "axios";
import paths from '../paths.json'
import { Button,Table } from "react-bootstrap";

const RealmUsers = ({client,token})=>{
    const isRun = useRef(false);
    const [users,setUsers] = useState([]);
    useEffect(()=>{
        if(isRun.current) return;
        isRun.current = true;
        axios.get(`http://localhost:2500/api/users`,{
            "headers":{
                "Authorization":`Bearer ${token}`
            }
        }).then(res=>setUsers(res.data)).catch(err=>console.error(err));
    },[])
    
    return(
        <Table variant="dark" striped bordered responsive hover>
        <thead>
            <tr>
            <th>User</th>
            <th>Email</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>View Metrics</th>
            </tr>
        </thead>
        <tbody>
            {users.map((item) => (
            <tr key={item.id}>
                <td>{item.USERNAME}</td>
                <td>{item.EMAIL}</td>
                <td>{item.FIRST_NAME}</td>
                <td>{item.LAST_NAME}</td>
                <td>method for changing to users metrics</td>
            </tr>
            ))}
        </tbody>
    </Table>
    )

}

export default RealmUsers;