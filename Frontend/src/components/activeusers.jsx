import react,{useEffect,useState} from 'react'
import {Table} from 'react-bootstrap'
import {Button} from 'react-bootstrap'
import axios from 'axios'
//still need to write logout function
function ForceLogout(username){
    //need to figure out how to implement this
}

const ActiveUsers = ()=>{
    const [users,setUsers] = useState([]);
    useEffect(()=>{
        //url is  a placeholder
        axios.get('https://backend.local',{
        
        }).then(response => response.json())
            .then(users =>setUsers(users))
            .catch(error => console.error('error'))
    },[])

    return(
        <Table striped bordered hover>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Username</th>
                    <th>Email</th>
                    <th>First Name</th>
                    <th>Last Name</th>
                    <th>Anomaly</th>
                    <th>sign out</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>1</td>
                    <td>gar7mn</td>
                    <td>gar7mn@missouri.edu</td>
                    <td>Grant</td>
                    <td>Richardet</td>
                    <td>Type speed</td>
                    <td><Button variant='danger'>Sign out</Button></td>
                </tr>
            </tbody>
            <tbody>
                {users.map(user=>{
                    <tr key={user.id}>
                        <td>{user.id}</td>
                        <td>{user.username}</td>
                        <td>{user.email}</td>
                        <td>{user.firstname}</td>
                        <td>{user.lastname}</td>
                        <td>{user.anomaly}</td>
                        <td><Button variant='danger'>Log Out</Button></td>
                    </tr>
                })}
            </tbody>
        </Table>
    )

}


export default ActiveUsers