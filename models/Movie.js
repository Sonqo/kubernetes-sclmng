const mongoose = require('mongoose');

const movieSchema = new mongoose.Schema({
    id: {
        type: Number,
        required: true,
    },
    title: {
        type: String,
        required: true,
    },
});

const Movie = mongoose.model('Movies', movieSchema, 'Movies');

module.exports = Movie;
