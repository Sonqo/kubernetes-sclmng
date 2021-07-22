const express = require('express');

const home = require('./routes/home');

const dbConfig = require('./config/database-config');

const server = express();
server.use(express.urlencoded({ extended: true }));
server.use(express.json());

const baseUrl = '/api';
server.use(`${baseUrl}/`, home);

const port = 3000;
server.listen(port, () => {
    console.log(`Server listening on port ${port}`);
});
