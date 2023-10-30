const mongoose = require('mongoose');

const LogSchema = new mongoose.Schema({
    scan: {type: String},
    logFile: [{
        type: String
    }],
}, {timestamps: true});

module.exports.Log = mongoose.model("Log", LogSchema);