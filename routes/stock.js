const mongoose = require('mongoose');
const router = require('express').Router();

const Pfizer = require('../models/Pfizer');

const dbConfig = require('../config/database-config');

mongoose
    .connect(dbConfig.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .catch((err) => console.error('Problem connecting to Mongo', err));

router.get('/show', (req, res) => {
    Pfizer.findOne({
        Date: { $gte: req.body.s_Date, $lt: req.body.e_Date },
    }).then(async (stock) => {
        if (!stock) {
            res.sendStatus(403);
        } else {
            docs = await Pfizer.find({ Date: { $gte: req.body.s_Date, $lt: req.body.e_Date } });
            res.send(docs);
        }
    });
});

module.exports = router;
