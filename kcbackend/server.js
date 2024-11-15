const dotenv = require('dotenv').config();
const express = require('express');
const app = express()
const Maketables = require('./db/queries')
const keycloak = require('./middlewares/keycloak')
const cors = require('cors');
const connection = require('./db/connect');
app.use(express.json())
//enable the keycloak middleware
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
app.get('/api/activeusers',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM ')
})
//endpoint that lists all users
app.get('/api/users',keycloak.protect('realm:Admin'),(req,res)=>{
    connection.query('SELECT * FROM USER_ENTITY;',(err,result,fields)=>{
        res.status(200).json(result);
    })
})
app.get('/api/user/:username',keycloak.protect('realm:Admin'),(req,res)=>{
    try{
        //Ensure the username parameter is not null
        if (req.params.username != null) {
            console.log(req.params.username)
            connection.query('SELECT * FROM USER_ENTITY WHERE USERNAME = ?',[req.params.username],(err,result,fields)=>{
                console.log(result);
                res.json(result);
            })
        }
        //handle the instance whena  username is null
        else{
            res.status(400).json({error:"username is required"});
        }
    }
    //catch other errors
    catch(error){
        console.log('some thing went wrong:',error);
        res.status(500).json({error:"Internal Server Error"});
    }
})
//words per min api endpoint
app.get('/api/wpm',keycloak.protect(),(req,res)=>{
    let query = 'SELECT a.USERNAME, b.value FROM USER_ENTITY a, wpm b WHERE a.ID = b.USER_ID and a.USERNAME =(?)';
    connection.query('SELECT * FROM wpm ORDER BY created_at DESC LIMIT 30;',(err,result,fields)=>{
        res.json(result);
    })
})
//needs testing
app.get('/api/wpm/:userid',(req,res)=>{
    console.log("check");
    try{
        if (req.params.userid) {
            connection.query('SELECT * FROM  wpm WHERE USER_ID = ? ORDER BY created_at DESC LIMIT 30;',[req.params.userid],(err,results,fields)=>{
                res.json(results);
            })
        }
    }catch(error){
        console.log(error);
        res.status(500).json({error:"Internal server error"});
    }
})
//mouse speed endpoint
app.get('/api/mousespeed',keycloak.protect(),(req,res)=>{
    let query = 'SELECT a.USERNAME, b.value,b.created_at FROM USER_ENTITY a ,mouse_speed b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM mouse_speed ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
})
app.get('/api/mousespeed/:userid',keycloak.protect('realm:Admin'),(req,res)=>{
    try{
        if (req.params.userid) {
            //new insertions every ten seconds of activity.
            connection.query("SELECT * FROM mouse_speed WHERE USER_ID = ? ORDER BY created_at DESC LIMIT 6;",[req.params.userid],(err,result,fields)=>{
                res.json(result);
            })
        }
    }
    catch(error){
        console.log(error);
        res.status(500).json({error:"internal server error"});
    }
})
//test methods of selecting users to display their metrics for the admin dashboard
app.get('/api/userselect',keycloak.protect('realm:Admin'),(req,res)=>{

    
})  

app.get('/api/clickdwelltime',keycloak.protect(),(req,res)=>{
    //will likely change the 30 after I talk with Jack.
    let query = 'SELECT * FROM  avg_click_dwell_time ORDER BY created_at DESC LIMIT 30;';

    connection.query('SELECT * FROM  avg_click_dwell_time ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    
    })
})
//aver dwell time api endpoint
app.get('/api/avgdwelltime',keycloak.protect(),(req,res)=>{
    let query = 'SELECT a.USERNAME,b.VALUE FROM USER_ENTITY a, avg_dwell_time b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM avg_dwell_time ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
});
//api method for getting the average time between keystrokes.
app.get('/api/time_between_strokes',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM avg_time_between_keystrokes ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
    
        res.json(result);
    })
})
app.get('/api/keys_per_sec',keycloak.protect(),(req,res)=>{
    let query = 'SELECT a.USERNAME, b.value,b.created_at FROM USER_ENTITY a , keys_per_sec b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM keys_per_sec ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
})
//figure out how we are displaying percentages
app.get('/api/percentages',keycloak.protect(),(req,res)=>{
    connection.query('SELECT * FROM percentages;',(err,result,fields)=>{
        res.json(result);
    
    })
})
//listen on the port
app.listen(port,console.log(`listening on port: ${port}`));
