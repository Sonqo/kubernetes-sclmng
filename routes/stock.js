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
    Stock.findOne({
        Date: { $gte: req.body.s_Date, $lt: req.body.e_Date },
    }).then(async (stock) => {
        if (!stock) {
            res.sendStatus(403);
        } else {
            docs = await Stock.find({ Date: { $gte: req.body.s_Date, $lt: req.body.e_Date } });
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
    newStock
        .save()
        .then((stock) => res.json(stock))
        .catch((err) => console.log(err));
});

module.exports = router;
