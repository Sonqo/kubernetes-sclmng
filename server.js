const express = require('express');
const mongoose = require('mongoose');

const home = require('./routes/home');
const data = require('./routes/data');

const dbConfig = require('./config/database-config');

const server = express();
server.use(express.urlencoded({ extended : true }));
server.use(express.json());

mongoose.connect(dbConfig.url, {
    useNewUrlParser: true
}).then(() => {
    console.log('Successfully connected to database');
}).catch(err => {
    console.log("Could not connect to database");
});

const baseUrl = '/node-app/api';
server.use(`${baseUrl}/`, home);
server.use(`${baseUrl}/data`, data);

const port = 3000;
server.listen(port, () => {
    console.log(`Server listening on port ${port}`)
});
