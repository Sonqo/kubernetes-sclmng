const mongoose = require('mongoose');
const router = require('express').Router();

const Ride = require('../models/Ride');

const dbConfig = require('../config/database-config');

mongoose
    .connect(dbConfig.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
        db: {
            readPreference: 'nearest',
        },
    })
    .catch((err) => console.error('Problem connecting to Mongo', err));

router.get('/show', async (req, res) => {
    docs = await Ride.find({
        started_at: { $gte: req.body.s_Date, $lt: req.body.e_Date },
        start_lat: { $gte: 40, $lt: 50 },
        start_lng: { $gte: -90, $lt: -85 },
        start_station_id: { $gte: 200, $lt: 250 },
        member_casual: 'member',
    }).read('nearest');
    if (!docs) {
        res.sendStatus(403);
    } else {
        res.send(docs);
    }
});

module.exports = router;
