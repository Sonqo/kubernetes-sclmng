const mongoose = require('mongoose');
const router = require('express').Router();

const Ride = require('../models/Ride');

const dbConfig = require('../config/database-config');

mongoose
    .connect(dbConfig.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .catch((err) => console.error('Problem connecting to Mongo', err));

router.get('/show', async (req, res) => {
    docs = await Ride.find({
        started_at: { $gte: req.body.s_Date, $lt: req.body.e_Date },
        member_casual: 'member',
    });
    if (!docs) {
        res.sendStatus(403);
    } else {
        res.send(docs);
    }
});

module.exports = router;
