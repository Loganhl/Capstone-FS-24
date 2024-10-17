const express = require('express')
const app = express();
const PORT = 2500




app.get('/api/activeusers',(req,res)=>{
  if (req.params.id != null) {
    // connection.query("SELECT a.USERNAME b.USER_ID FROM USER_ENTITY a OFFLINE_USER_SESSION b WHERE a.ID = b.USER_ID",(err,result,fields)=>{
    //   res.json(result);   
    // })
    res.send("hello");
  }
  res.send("hello");
})

app.listen(PORT,console.log(`app listening on port ${PORT}`))