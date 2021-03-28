const express = require('express');
const mongoose = require('mongoose');

const app = express();
app.use(express.urlencoded({ extended : true }));
app.use(express.json());

const dbConfig = require('./config/database-config');

mongoose.connect(dbConfig.url, {
    useNewUrlParser: true
}).then(() => {
    console.log('Successfully connected to database');
}).catch(err => {
    console.log("Could not connect to database");
})

app.get('/', (req, res) => {
    res.send("Welcome to Node-App!")
})

const port = 3000
app.listen(port, () => {
    console.log(`Server listening on port ${port}`)
})
