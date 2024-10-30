const express = require('express')
const mysql = require('mysql2')
const app = express();
const PORT = 2500
const cors = require('cors')
const keycloak = require('./middlewares/keycloak')
const axios = require('axios')
const session = require("express-session");
const memorystore = new session.MemoryStore()
const dotenv = require('dotenv')
dotenv.configDotenv('./.env')
// const Keycloak  = require("keycloak-connect")
// const keycloak = new Keycloak({
    
// })

// app.use(session({
//   "secret":process.env.KEYCLOAK_CLIENT_SECRET,
//   "resave":false,
//   "saveUninitialized":true,
//   "store":memorystore,
//   "cookie":{
//     "sameSite":"none"
//   }
// }))
app.use(keycloak.middleware())
// console.log(keycloak.checkSso())
// const tokenreq = {
//   hostname: 'localhost',
//   port:80,
//   path:'/realms/biovault/protocol/openid-connect/token',
//   method: 'POST',
//   headers:{
//     'Content-Type':'x-www-form-urlencoded'
//   }
// }
const connection = mysql.createConnection({

  "user":process.env.SQL_USER,
  "password":process.env.SQL_PASS,
  "database":process.env.SQL_DB,
  "host":process.env.SQL_HOST,
  "port":process.env.SQL_PORT
})
// keycloak.storeGrant(keycloak.grantManager.createGrant({
//   "access_token":""
// }))

// const authreq = axios.post("http://localhost/realms/biovault/protocol/openid-connect/token",{
//    'grant_type':'client_credentials',
//    "client_id":"backend",
//    "client_secret":"a8F6I5FV1O9VF1EdreOvOQGvVDP415cQ"
// },{
//   "headers":{
//     "Content-Type":"application/x-www-form-urlencoded",
//   }
// }).then((resp => console.log(resp.data)))
// keycloak.grantManager.obtainDirectly('gar7mn','Wand4511').then((resp=>keycloak.grantManager.ensureFreshness(resp)));
keycloak.grantManager.obtainFromClientCredentials().then((grant=> keycloak.grantManager.validateGrant(grant).then(keycloak.grantManager.ensureFreshness(grant))))

// authreq.then((resp => console.log(resp.data)))
// authreq.then((resp)=>session({
//   "saveUninitialized":false,
//   "secret":resp.data.access_token,
//   "cookie":{
//     "secure":"auto",
//     "signed":true
//   }
// }))

// keycloak.storeGrant({
//   "access_token":resp.data.access_token,
//   "refresh_token":resp.data.refresh_token,
//   "expires_in":60,
// })
app.use(cors({}))
app.post('/api/forcelogout',keycloak.protect(),(req,res)=>{
    let user = req.body.user;
    //post logout message
    res.status(200).send("success");
})

app.use(express.json())
app.get('/api/users',keycloak.protect(),(req,res)=>{
  connection.query("SELECT * FROM USER_ENTITY;",(err,result,fields)=>{
    console.log(result);
    res.json(result);
  })
})
app.get('/api',(req,res)=>{
  res.json({"welcome":"To the biovault backend"});
})
app.get('/api/sec',keycloak.protect("realm:admin"),(req,res)=>{
  res.json({"area":"secure"});
})
app.post('/api/mousedata:userid',keycloak.protect(),(req,res)=>{
  if (req.params.userid != null) {
    let data_id = req.body.data_id;
    let user_id = req.params.userid;
    let avg_speed = req.body.avg_speed;
    let avg_click_dwell = req.body.avg_click_dwell;
    let avg_double_click = req.body.avg_double_click;
    let query = 'INSERT INTO MouseData (data_id,user_id,avg_speed,avg_click_dwell,avg_double_click) VALUES (?,?,?,?);'
    connection.query(query,[data_id,user_id,avg_speed,avg_click_dwell.avg_double_click],(err,result,fields)=>{
      res.json(result);
    })
  }
})
app.post('/api/keyboarddata:userid',keycloak.protect(),(req,res)=>{
    if (req.params.userid != null) {
      let data_id = req.body.data_id
      let user_id = req.body.user_id
      let wpm = req.body.wpm
      let keystrokes_per_10_sec = req.body.keystrokes_per_10_sec
      let keys_per_second = req.body.keys_per_second;
      let query = "INSERT into KeyboardData (data_id,user_id,wpm,keystrokes_per_10_sec,keys_per_second) VALUES (?,?,?,?,?);"
      connection.query(query,[data_id,user_id,wpm,keystrokes_per_10_sec,keys_per_second],(err,result,fields)=>{
        res.json(result);
      })
      res.json("succseffully logged anomaly")
    }
    if(req.params.userid == null){
      res.json({"expected user_id parameter":"got none"})
    }
})
app.post('/api/click_hotspots:user_id',keycloak.protect(),(req,res)=>{
  if (req.params.user_id != null) {
    let hotspot_id = req.body.hotspot_id;
    let user_id = req.body.user_id;
    let x_coordinate = req.body.x_coordinate;
    let y_coordinate = req.body.y_coordinate;
    let timestamp = req.body.timestamp;
    let num_clicks = req.body.num_clicks;
    let query = 'INSERT INTO ClickHotspots (hotspot_id,user_id,x_coordinate,y_coordinate,CURRENT_TIMESTAMP,num_clicks) VALUES(?,?,?,?,?,?)'
    //execute the query
    connection.query(query,[hotspot_id,user_id,x_coordinate,y_coordinate,timestamp,num_clicks],(err,result,fields)=>{
      res.json(result);
    })
  }
})
app.get('/secured',keycloak.protect(),(req, res) => {
  console.log("hello");
  res.json({message: 'secured'});
});

app.get('/api/activeusers',keycloak.protect(),(req,res)=>{
  connection.query("SELECT a.USERNAME,a.EMAIL,a.FIRST_NAME,a.LAST_NAME, b.USER_ID FROM USER_ENTITY a, OFFLINE_USER_SESSION b WHERE a.ID = b.USER_ID",(err,result,fields)=>{
      res.json(result);     
    })

})
app.get('/api/userinfo:userid',keycloak.protect(),(req,res)=>{
  if (req.params.userid != null) {
    res.json({"Error":"not set up yet"})
  }
})
app.get('/api/keyboarddata:userid',keycloak.protect(),(req,res)=>{
  //may end up deleting this one
  res.json({"error":"this is not set up yet"})
})
app.listen(PORT,console.log(`app listening on port ${PORT}`))