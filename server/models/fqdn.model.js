const mongoose = require('mongoose');

const FqdnSchema = new mongoose.Schema({
    fqdn: {type:String},
    recon: {
        subdomains: {
            gospider: [{
                type: String
            }],
            hakrawler: [{
                type: String
            }],
            subdomainizer: [{
                type: String
            }],
            sublist3r: [{
                type: String
            }],
            amass: [{
                type: String
            }],
            assetfinder: [{
                type: String
            }],
            gau : [{
                type: String
            }],
            ctl : [{
                type: String
            }],
            shosubgo : [{
                type: String
            }],
            subfinder : [{
                type: String
            }],
            githubSearch : [{
                type: String
            }],
            shuffledns : [{
                type: String
            }],
            shufflednsCustom : [{
                type: String
            }],
            cloudRanges : [{
                type: String
            }],
            consolidated : [{
                type: String
            }],
            consolidatedNew : [{
                type: String
            }],
            httprobe : [{
                type: String
            }],
            httprobeAdded : [{
                type: String
            }],
            httprobeRemoved : [{
                type: String
            }],
            masscan : [{
                type: String,
            }],
            masscanAdded : [{
                type: String
            }],
            masscanRemoved : [{
                type: String
            }],
            masscanLive : [{
                type: String
            }]
        },
        osint: {
            notableRepos: [{
                type: String
            }],
            GithubSearch: [{
                payload: String,
                results: Number,
                url: String
            }],
            GithubUsers: [{
                username: String,
                githubUrl: String
            }],
            Google: [{
                type: String
            }],
            Shodan: [{
                type: String
            }],
            Censys: [{
                type: String
            }]
        }
    },
    vulns: [{
        impactful: {type: Boolean},
        host: {type: String},
        "template-id": {type: String},
        info: {
            author: [{
                type: String
            }],
            description: {type: String},
            name: {type: String},
            reference: [{
                type: String
            }],
            severity: {type: String},
            tags: [{
                type: String
            }]
        },
        "extracted-results": [{
            type: String
        }],
        ip: {type: String},
        "matched-at": {type: String},
        "matcher-name": {type: String},
        timestamp: {type: String},
        type: {type: String},
        "curl-command":{type: String},
    }],
    targetUrls: [{
        type: String
    }],
    ips: [{
        ip: {type: String},
        ports: [{
            type: String
        }]
    }]
}, {timestamps: true});

module.exports.Fqdn = mongoose.model("Fqdn", FqdnSchema);