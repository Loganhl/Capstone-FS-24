const dotenv = require('dotenv').config();
const express = require('express');
const app = express()
const Maketables = require('./db/queries')
const mysql = require('mysql2')
const keycloak = require('./middlewares/keycloak')
const cors = require('cors');
const connection = require('./db/connect');
app.use(express.json())
app.use(keycloak.middleware())
app.use(cors())

const port = 2500;
//authenticate with the client
keycloak.grantManager.obtainFromClientCredentials().then((grant=> keycloak.grantManager.validateGrant(grant).then(keycloak.grantManager.ensureFreshness(grant))))
// make the tables if they do not already exist

Maketables();
app.get('/api',(req,res)=>{
    res.json({
        "Luke":"I am Your Father."
    });
})
//endpoint that lists all users
app.get('/api/users',keycloak.protect(),(req,res)=>{
    res.json({
        "resp":"Access Granted"
    })
})
//words per min api endpoint
app.get('/api/wpm',keycloak.protect(),(req,res)=>{

    connection.query('SELECT * FROM wpm;',(err,result,fields)=>{
        res.json(result)
    })
})
//mouse speed endpoint
app.get('/api/mousespeed',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM mouse_speed;',(err,result,fields)=>{
        res.json(result);
    })
})
//aver dwell time api endpoint
app.get('/api/avgdwelltime',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM avg_dwell_time;',(err,result,fields)=>{
        res.json(result);
    })
});

app.get('/api/keys_per_sec',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM keys_per_sec;',(err,result,fields)=>{
        res.json(result);
    })
})
//listen on the port
app.listen(port,console.log(`listening on port: ${port}`));