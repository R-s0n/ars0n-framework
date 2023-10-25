const mongoose = require('mongoose');

const FqdnSchema = new mongoose.Schema({
    fqdn: {type:String},
    dns: {
        arecord: [{
            type: String
        }],
        aaaarecord: [{
            type: String
        }],
        cnamerecord: [{
            type: String
        }],
        mxrecord: [{
            type: String
        }],
        txtrecord: [{
            type: String
        }],
        node: [{
            type: String
        }],
        nsrecord: [{
            type: String
        }],
        srvrecord: [{
            type: String
        }],
        ptrrecord: [{
            type: String
        }],
        spfrecord: [{
            type: String
        }],
        soarecord: [{
            type: String
        }]
    },
    aws: {
        s3: [{
            domain: {type: String},
            public: {
                type: Boolean,
                default: false
            },
            downloadExploit: {
                type: Boolean,
                default: false
            },
            uploadExploit: {
                type: Boolean,
                default: false
            },
            authenticated: {
                type: Boolean,
                default: false
            },
            subdomainTakeover: {
                type: Boolean,
                default: false
            },
            files: [{
                type: String
            }]
        }],
        ec2: [{
            type: String
        }],
        cloudfront: [{
            type: String
        }],
        elb: [{
            type: String
        }],
        documentdb: [{
            type: String
        }],
        api_gateway: [{
            type: String
        }],
        elasticbeanstalk: [{
            type: String
        }]
    },
    azure: {
        placeholder: {type: String}
    },
    gcp: {
        placeholder: {type: String}
    },
    ips: [{
        ip: {type: String},
        ports: [{
            type: String
        }]
    }],
    subnets: [{
        type: String
    }],
    asns: [{
        type: String
    }],
    isps: [{
        type: String
    }],
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
    vulnsSSL: [{
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
    vulnsFile: [{
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
    vulnsDNS: [{
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
    vulnsVulns: [{
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
    vulnsTech: [{
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
    vulnsMisconfig: [{
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
    vulnsCVEs: [{
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
    vulnsCNVD: [{
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
    vulnsExposed: [{
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
    vulnsExposure: [{
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
    vulnsMisc: [{
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
    vulnsNetwork: [{
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
    vulnsRs0n: [{
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
    vulnsHeadless: [{
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
    }]
}, {timestamps: true});

module.exports.Fqdn = mongoose.model("Fqdn", FqdnSchema);