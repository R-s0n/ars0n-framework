const mongoose = require('mongoose');

const UrlSchema = new mongoose.Schema({
    url: {type: String},
    fqdn: {type: String},
    endpoints: [{
        endpoint: String,
        statusCode: Number,
        responseLength: Number,
        arjun: {
            method: String,
            params: [{
                type: String
            }]
        },
        arjunPost: {
            method: String,
            params: [{
                type: String
            }]
        },
        arjunJson: {
            method: String,
            params: [{
                type: String
            }]
        }
    }],
    completedWordlists: [{
        type: String
    }],
}, {timestamps: true});

module.exports.Url = mongoose.model("Url", UrlSchema);