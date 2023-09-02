const mongoose = require('mongoose');

const UrlSchema = new mongoose.Schema({
    url: {type: String},
    fqdn: {type: String},
    endpoints: [{
        endpoint: String,
        httpVerb: {
            type: String,
            enum: ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"],
            default: "GET"
        },
        statusCode: Number,
        responseLength: Number,
    }],
}, {timestamps: true});

module.exports.Url = mongoose.model("Url", UrlSchema);