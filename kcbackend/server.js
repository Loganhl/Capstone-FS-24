const dotenv = require('dotenv').config();
const express = require('express');
const app = express()
const Maketables = require('./db/queries')
const keycloak = require('./middlewares/keycloak')
const cors = require('cors');
const connection = require('./db/connect');
const session = require('express-session')
const crypto = require('crypto')
app.use(express.json())
//enable the keycloak middlewares
app.use(keycloak.middleware())
app.use(cors());
const secret = crypto.randomBytes(64).toString('hex')
const port = 2500;
//authenticate with the client
keycloak.grantManager.obtainFromClientCredentials().then((grant=> keycloak.grantManager.validateGrant(grant).then(keycloak.grantManager.ensureFreshness(grant))))
// make the tables if they do not already exist
app.use(session({
    "name":"localhost",
    "store":session.MemoryStore(),
    "secret":secret,
    "cookie":{secure:false,"signed":true,"httpOnly":false,"priority":"high","path":"/api/*"},
    "resave":true,
    "saveUninitialized":false,
    
}))
Maketables();
app.get('/api',(req,res)=>{
    res.json({
        "Luke":"I am Your Father."
    });
})
app.get('/api/activeusers',(req,res)=>{
    connection.query('SELECT * FROM ')
})
//endpoint that lists all users
app.get('/api/users',(req,res)=>{
    connection.query('select a.username, a.EMAIL,a.FIRST_NAME,a.LAST_NAME  ,a.ID from USER_ENTITY a, REALM b WHERE  a.REALM_ID = b.ID AND b.NAME = "biovault" AND a.LAST_NAME =0;',(err,result,fields)=>{
        res.status(200).json(result);
    })
})
app.get('/api/user/:username',(req,res)=>{
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
app.get('/api/wpm',(req,res)=>{
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
app.get('/api/mousespeed',(req,res)=>{
    let query = 'SELECT a.USERNAME, b.value,b.created_at FROM USER_ENTITY a ,mouse_speed b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM mouse_speed ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
})
app.get('/api/mousespeed/:userid',(req,res)=>{
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
app.get('/api/userselect',(req,res)=>{

    
})  

app.get('/api/clickdwelltime',(req,res)=>{
    //will likely change the 30 after I talk with Jack.
    let query = 'SELECT * FROM  avg_click_dwell_time ORDER BY created_at DESC LIMIT 30;';

    connection.query('SELECT * FROM  avg_click_dwell_time ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    
    })
})
//aver dwell time api endpoint
app.get('/api/avgdwelltime',(req,res)=>{
    let query = 'SELECT a.USERNAME,b.VALUE FROM USER_ENTITY a, avg_dwell_time b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM avg_dwell_time ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
});
//api method for getting the average time between keystrokes.
app.get('/api/time_between_strokes',(req,res)=>{
    connection.query('SELECT * FROM avg_time_between_keystrokes ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
    
        res.json(result);
    })
})
app.get('/api/keys_per_sec',(req,res)=>{
    let query = 'SELECT a.USERNAME, b.value,b.created_at FROM USER_ENTITY a , keys_per_sec b WHERE a.ID = b.USER_ID AND a.USERNAME = (?);';
    connection.query('SELECT * FROM keys_per_sec ORDER BY created_at DESC LIMIT 6;',(err,result,fields)=>{
        res.json(result);
    })
})
app.get('/api/keys_per_sec:userid',(req,res)=>{
    try{
        if (req.params.userid) {
            connection.query("SELECT * FROM keys_per_sec WHERE a.USERID = ? ORDER BY DESC LIMIT 60;",[req.params.userid],(err,result,fields)=>{
                res.json(result);
            });
        }
        else{
            res.status(500).json({"error":"Internal Server Error"})
        }
    }catch(err){
        console.log(err);
    }
})
//figure out how we are displaying percentages
app.get('/api/percentages',(req,res)=>{
    connection.query('SELECT * FROM percentages;',(err,result,fields)=>{
        res.json(result);
    
    })
})
//listen on the port
app.listen(port,console.log(`listening on port: ${port}`));
