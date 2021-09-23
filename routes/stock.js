const mongoose = require('mongoose');
const router = require('express').Router();

const dbConfig = require('../config/database-config');

const Stock = require('../models/Pfizer');

mongoose
    .connect(dbConfig.url, {
        useNewUrlParser: true,
        useUnifiedTopology: true,
    })
    .catch((err) => console.error('Problem connecting to Mongo', err));

router.get('/show', (req, res) => {
    Movie.findOne({
        id: req.body.id,
    }).then(async (user) => {
        if (!user) {
            res.sendStatus(403);
        } else {
            docs = await Movie.find({ Date: req.body.Date });
            res.send(docs);
        }
    });
});

router.post('/add', (req, res) => {
    const newStock = new Stock({
        Date: req.body.Date,
        Open: req.body.Open,
        High: req.body.High,
        Low: req.body.Low,
        Close: req.body.Close,
        'Adj Close': req.body['Adj Close'],
        Volume: req.body.Volume,
    });
    newMovie
        .save()
        .then((movie) => res.json(movie))
        .catch((err) => console.log(err));
});

module.exports = router;
