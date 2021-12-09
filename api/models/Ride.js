const mongoose = require('mongoose');

const rideSchema = new mongoose.Schema({
    ride_id: {
        type: String,
        required: true,
    },
    rideable_type: {
        type: String,
        required: true,
    },
    started_at: {
        type: String,
        required: true,
    },
    ended_at: {
        type: String,
        required: true,
    },
    start_station_name: {
        type: String,
        required: true,
    },
    start_station_id: {
        type: Number,
        required: true,
    },
    end_station_name: {
        type: String,
        required: true,
    },
    end_station_id: {
        type: Number,
        required: true,
    },
    start_lat: {
        type: Number,
        required: true,
    },
    start_lng: {
        type: Number,
        required: true,
    },
    end_lat: {
        type: Number,
        required: true,
    },
    end_lng: {
        type: Number,
        required: true,
    },
    member_casual: {
        type: String,
        required: true,
    },
});

const Ride = mongoose.model('Ride', rideSchema, 'Ride');

module.exports = Ride;
