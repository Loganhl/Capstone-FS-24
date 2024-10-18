const express = require('express')
const mysql = require('mysql2')
const app = express();
const PORT = 2500
const cors = require('cors')
const connection = mysql.createConnection({

  "user":"root",
  "password":"secretsquirrels",
  "database":"biometric_auth",
  "host":"mysql",
})
app.use(cors())
app.use(express.json())
app.get('/api/users',(req,res)=>{
  connection.query("SELECT * FROM USER_ENTITY;",(err,result,fields)=>{
    res.json(result);
  })
})

app.get('/api/activeusers',(req,res)=>{
  if (req.params.id != null) {
    connection.query("SELECT a.USERNAME b.USER_ID FROM USER_ENTITY a OFFLINE_USER_SESSION b WHERE a.ID = b.USER_ID",(err,result,fields)=>{
      res.json(result);   
    })
    res.send("hello");
  }
  res.send("hello");
})

app.listen(PORT,console.log(`app listening on port ${PORT}`))