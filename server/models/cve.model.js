const mongoose = require('mongoose');

const UrlSchema = new mongoose.Schema({
    cve: {type: String},
    javascript: {type: Boolean},
    searchTerm: {type: String},
    blacklistTerms: [{
        type: String
    }]
}, {timestamps: true});

module.exports.Cve = mongoose.model("Cve", UrlSchema);