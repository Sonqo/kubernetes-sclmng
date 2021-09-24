const mongoose = require('mongoose');

const stockSchema = new mongoose.Schema({
    Date: {
        type: String,
        required: true,
    },
    Open: {
        type: Number,
        required: true,
    },
    High: {
        type: Number,
        required: true,
    },
    Low: {
        type: Number,
        required: true,
    },
    Close: {
        type: Number,
        required: true,
    },
    'Adj Close': {
        type: Number,
        required: true,
    },
    Volume: {
        type: Number,
        required: true,
    },
});

const Stock = mongoose.model('Pfizer', stockSchema, 'Pfizer');

module.exports = Stock;
