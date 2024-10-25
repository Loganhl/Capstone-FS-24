const express = require('express')
const mysql = require('mysql2')
const app = express();
const PORT = 2500
const cors = require('cors')
const keycloak = require('./middlewares/keycloak')
keycloak.getConfig()
keycloak.loginUrl()
const connection = mysql.createConnection({

  "user": "root",
  "password":"secretsquirrels",
  "database":"biometric_auth",
  "host":"localhost",
  "port":"3307"
})

app.use(cors())
app.use(keycloak.middleware())
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
app.get('/api/sec',keycloak.protect(),(req,res)=>{
  res.json({"area":"secure"});
})
app.post('/api/mousedata:userid',(req,res)=>{
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
app.post('/api/keyboarddata:userid',(req,res)=>{
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
app.get('/secured', keycloak.protect('realm:user'), (req, res) => {
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
app.get('/api/keyboarddata:userid',(req,res)=>{
  //may end up deleting this one
  res.json({"error":"this is not set up yet"})
})
app.listen(PORT,console.log(`app listening on port ${PORT}`))