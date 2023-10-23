const { Fqdn } = require("../models/fqdn.model");
const { Url } = require("../models/url.model");
const { Cve } = require("../models/cve.model");
const { Log } = require("../models/log.model");
const util = require('util');
const exec = require('child_process').exec;
const spawn = require('child_process').spawn;
const execFile = require('child_process').execFile;
const execSync = util.promisify(require('child_process').execSync);
const axios = require('axios');
const https = require('https');

module.exports.ping = (req, res) => {
    res.json({ message: "pong" });
}

// CVE Controllers

module.exports.addCve = (req, res) => {
    
    Cve.create(req.body)
        .then(newCve=>res.json(newCve))
        .catch(err=>res.status(400).json(err))
}

module.exports.getCves = (req, res) => {
    
    Cve.find()
        .then(Cves=>res.json(Cves))
        .catch(err=>res.status(400).json(err))
}

module.exports.deleteCve = (req, res) => {
    
    Cve.deleteOne({ cve: req.body.cve })
        .then(result=>res.json({success:true}))
        .catch(err=>res.status(400).json(err))
}

// Fqdn Controllers

module.exports.addFqdn = (req, res) => {
    
    Fqdn.create(req.body)
        .then(newFqdn=>res.json(newFqdn))
        .catch(err=>res.status(400).json(err))
}

module.exports.getFqdns = (req, res) => {
    
    Fqdn.find()
        .then(fqdns=>res.json(fqdns))
        .catch(err=>res.status(400).json(err))
}

module.exports.getFqdn = (req, res) => {
    
    Fqdn.findOne({ _id: req.body._id })
        .then(oneFqdn=>res.json(oneFqdn))
        .catch(err=>res.status(400).json(err))
}

module.exports.deleteFqdn = (req, res) => {
    
    Fqdn.deleteOne({ _id: req.body._id })
        .then(result=>res.json({success:true}))
        .catch(err=>res.status(400).json(err))
}

module.exports.updateFqdn = (req, res) => {
    console.log(req.body)
    Fqdn.findOneAndUpdate(
        { _id: req.body._id },
        req.body,
        { new: true, runValidators: true })
        .then(result=>res.json(result))
        .catch(err=>res.status(400).json(err))
}

module.exports.autoGetFqdn = (req, res) => {
    
    Fqdn.findOne({ fqdn: req.body.fqdn })
        .then(oneFqdn=>res.json(oneFqdn))
        .catch(err=>res.status(400).json(err))
}

module.exports.autoUpdateFqdn = (req, res) => {
    
    Fqdn.findOneAndUpdate(
        { fqdn: req.body.fqdn },
        req.body,
        { new: true, runValidators: true })
        .then(result=>res.json(result))
        .catch(err=>res.status(400).json(err))
}

// Url Controllers

module.exports.addUrl = (req, res) => {
    
    Url.create(req.body)
        .then(newUrl=>res.json(newUrl))
        .catch(err=>res.status(400).json(err))
}

module.exports.getUrls = (req, res) => {
    
    Url.find()
        .then(urls=>res.json(urls))
        .catch(err=>res.status(400).json(err))
}

module.exports.getUrl = (req, res) => {
    
    Url.findOne({ _id: req.body._id })
        .then(oneUrl=>res.json(oneUrl))
        .catch(err=>res.status(400).json(err))
}

module.exports.deleteUrl = (req, res) => {
    
    Url.deleteOne({ _id: req.body._id })
        .then(result=>res.json({success:true}))
        .catch(err=>res.status(400).json(err))
}

module.exports.updateUrl = (req, res) => {
    
    Url.findOneAndUpdate(
        { _id: req.body._id },
        req.body,
        { new: true, runValidators: true })
        .then(result=>res.json(result))
        .catch(err=>res.status(400).json(err))
}

module.exports.autoGetUrl = (req, res) => {
    
    Url.findOne({ url: req.body.url })
        .then(oneUrl=>res.json(oneUrl))
        .catch(err=>res.status(400).json(err))
}

module.exports.autoUpdateUrl = (req, res) => {
    
    Url.findOneAndUpdate(
        { url: req.body.url },
        req.body,
        { new: true, runValidators: true })
        .then(result=>res.json(result))
        .catch(err=>res.status(400).json(err))
}

module.exports.autoDeleteUrl = (req, res) => {
    
    Url.deleteOne({ url: req.body.url })
        .then(result=>res.json({success:true}))
        .catch(err=>res.status(400).json(err))
}

// Log Controllers

module.exports.addLog = (req, res) => {
    
    Log.create(req.body)
        .then(newLog=>res.json(newLog))
        .catch(err=>res.status(400).json(err))
}

module.exports.getLogs = (req, res) => {
    
    Log.find()
        .then(Logs=>res.json(Logs))
        .catch(err=>res.status(400).json(err))
}

module.exports.deleteLogs = (req, res) => {
    
    Log.deleteMany({scan: { $ne: "foo" }})
        .then(Logs=>res.json(Logs))
        .catch(err=>res.status(400).json(err))
}

// Scanning Controllers

const proxyConfig = {
    protocol: 'http',
    host: '127.0.0.1',
    port: 8080,
  };

async function fetchUrlsThroughProxy(urlList) {
    for (const url of urlList) {
        if (url.includes("https://")){
            continue;
        }
        try {
        const response = await axios.get(url, {
          proxy: proxyConfig
        });
      } catch (error) {
        console.error(`Error while fetching ${url}:`);
        console.error(error.message);
      }
    }
  }
    
module.exports.getHttpOnly = (req, res) => {
    fetchUrlsThroughProxy(req.body)
    .then((responses) => {
      console.log('All requests completed:');
      console.log(responses);
    })
    .catch((err) => {
      console.error('Error:', err);
    });
}

module.exports.populateBurp = (req, res) => {
    console.log(req.body)
    const burpScan = {
            urls: req.body,
            scan_configurations: [{
                type: "NamedConfiguration",
                name: "Crawl and Audit - Fast"
            }]
    }
    axios.post("http://127.0.0.1:1337/v0.1/scan", burpScan)
        .then((response) => {
            console.log('Response:', response.data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

module.exports.runBurpScanDefault = (req, res) => {
    console.log(req.body.targetUrl)
    const burpScan = {
            urls: [req.body.targetUrl]
    }
    axios.post("http://127.0.0.1:1337/v0.1/scan", burpScan)
        .then((response) => {
            console.log('Response:', response.data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}

module.exports.runBurpScanDeep = (req, res) => {
    console.log(req.body.targetUrl)
    const burpScan = {
            urls: [req.body.targetUrl],
            scan_configurations: [{
                type: "NamedConfiguration",
                name: "Crawl and Audit - Deep"
    }]
    }
    console.log(burpScan)
    axios.post("http://127.0.0.1:1337/v0.1/scan", burpScan)
        .then((response) => {
            console.log('Response:', response.data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
}