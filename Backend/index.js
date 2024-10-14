
const express = require('express')
const app = express()
const mysql = require('mysql2')
const cors = require('cors')
//create connection
// const connection =mysql.createConnection({
//     host:'http://localhost:3306',
//     database:'kc',
//     user:'root',
//     password:'Wand4511'
// });

app.use((req,res,next)=>{   
    
    res.setHeader("Access-Control-Allow-Origin","*");
    res.setHeader("Access-Control-Allow-Headers","Cross-Origin, X-Requested-With, Content-Type, Accept")
    res.setHeader("Access-Control-Allow-Methods","GET, POST, PATCH, DELETE, OPTIONS");

    next();
})


app.use(express.json());
app.use('/api/posts',(req,res,next)=>{
    const posts = [
        {
            id: "654664",
            title:"1: server post",
            content: "This is from the server"
        },
        {
            id:"654665",
            title:"2: server post",
            content: "this is from the server"
        },
        {
            id:"654666",
            title:"3: server post",
            content:"This is from the server"
        }
    ]
    // connection.query('SELECT * FROM post;',((n,results,fields)=>{
    //     console.log('hell');
    //     res.status(200) 
    // }))
    res.status(200).json({
        message: "this is fetched data",
        posts:posts
    });
    
    
    // console.log(posts);
})
let query = `INSERT INTO post
		( id,title, content) VALUES (?, ?, ?);`;

app.post('/api/test',(req,res,next)=>{
    console.log(req.body)
    let id = Date.now().toString()
    let title = req.body.title
    let content = req.body.content
    console.log(req.body.title)
    
    connection.query(query, [id,
        title,content], (err, rows) => {
            if (err) throw err;
            console.log("Row inserted with id = "
                + id);
                res.status(200)
        });
        res.status(200);
    const posts = [
        {
            id: "654664",
            title:"1: server post",
            content: "This is from the server"
        },
        {
            id:"654665",
            title:"2: server post",
            content: "this is from the server"
        },
        {
            id:"654666",
            title:"3: server post",
            content:"This is from the server"
        },
    ]
    // res.json(posts)
     
})
app.listen(4000)