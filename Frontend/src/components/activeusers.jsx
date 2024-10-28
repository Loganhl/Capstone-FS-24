import React,{useState,useEffect,useRef} from "react";
import axios from "axios";
import paths from '../paths.json'
import { Button,Table } from "react-bootstrap";

const ActiveUsers = ({client,token})=>{
    const isRun = useRef(false);
    const [users,setUsers] = useState([]);
    useEffect(()=>{
        if(isRun.current) return;
        isRun.current = true;
        axios.get(`http://localhost:2500/api/activeusers`,{
            "headers":{
                "Authorization":`Bearer ${token}`
            }
        }).then(res=>setUsers(res.data)).catch(err=>console.error(err));
    },[])
    return(
        <Table striped bordered hover>
        <thead>
            <tr>
            <th>Userid</th>
            <th>User</th>
            <th>Email</th>
            <th>First Name</th>
            <th>Last Name</th>
            <th>Sign Out</th>
            </tr>
        </thead>
        <tbody>
            {users.map((item) => (
            <tr key={item.id}>
                <td>{item.USER_ID}</td>
                <td>{item.USERNAME}</td>
                <td>{item.EMAIL}</td>
                <td>{item.FIRST_NAME}</td>
                <td>{item.LAST_NAME}</td>
                <td><Button variant="warning">Force Log out</Button></td>
            </tr>
            ))}
        </tbody>
    </Table>
    )

}

export default ActiveUsers;