import React,{useEffect,useState} from "react"
import axios from "axios";
import { Table,Button } from "react-bootstrap";
const  GetUsers  = ()=>{
    const [users,setusers] =useState([]);
    useEffect(()=>{
        axios.get('http://backend/api/users').then(response=>{
            setusers(response.data)
        }).catch(error=>{
            console.error(error)
        })
    },[])
    return(
        <Table>
            <thead>
                <tr>
                    <th>UserId</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                </tr>
            </thead>
            <tbody>
                {users.map((user)=>{
                    <tr key={user.id}>
                        <td>{user.ID}</td>
                        <td>{user.USERNAME}</td>
                        <td>{user.EMAIL}</td>
                        <td>{user.FIRST_NAME}</td>
                        <td>{user.LAST_NAME}</td>
                    </tr>
                })}
            </tbody>
        </Table>
    )
}