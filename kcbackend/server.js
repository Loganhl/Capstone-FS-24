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

keycloak.grantManager.obtainFromClientCredentials().then((grant=> keycloak.grantManager.validateGrant(grant).then(keycloak.grantManager.ensureFreshness(grant))))
Maketables();
app.get('/api',(req,res)=>{
    res.json({
        "Luke":"I am Your Father."
    });
})

app.get('/api/users',keycloak.protect(),(req,res)=>{
    res.json({
        "resp":"Access Granted"
    })
})
app.get('/api/mousespeed',keycloak.protect(),(req,res)=>{
    res.send("continue work here");
})
app.get('/api/avgdwelltime',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM avg_dwell_time;',(err,result,fields)=>{
        res.json(result);
    })
})

app.listen(port,console.log(`listening on port: ${port}`));

