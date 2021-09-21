const mongoose = require('mongoose');
const router = require('express').Router();

const dbConfig = require('../config/database-config');

const Movie = require('../models/Movie');

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
            docs = await Movie.find({ id: req.body.id });
            res.send(docs);
        }
    });
});

router.post('/add', (req, res) => {
    const newMovie = new Movie({
        id: req.body.id,
        title: req.body.title,
    });
    newMovie
        .save()
        .then((movie) => res.json(movie))
        .catch((err) => console.log(err));
});

module.exports = router;
