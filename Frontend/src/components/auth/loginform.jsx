import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import axios from 'axios';
function LoginForm() {
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async (e) => { e.preventDefault(); 
    try { 
        const response = await axios.post('http://localhost:2500/api/login', formData, 
        { 
            headers: { 'Content-Type': 'application/json', }, 
            
        }
        ); 
            console.log('Success:', response.data); } 
            catch (error) 
            { console.error('Error:', error); 

            } };

  return (
    <Form onSubmit={handleSubmit}>
      <Form.Group controlId="username">
    
        <Form.Control
          type="text"
          placeholder="Username"
          name="username"
          value={formData.username}
          onChange={handleChange}
        />
      </Form.Group>

      <Form.Group controlId="password">
        <Form.Control
          type="password"
          placeholder="password"
          name="password"
          value={formData.password}
          onChange={handleChange}
        />
      </Form.Group>


      <Button variant="primary" type="submit">
        Submit
      </Button>
    </Form>
  );
}

export default LoginForm;
