const Controller = require('../controllers/Controller');

module.exports = function(app){
    app.get('/api/ping', Controller.ping);

    app.post('/api/cve/all', Controller.getCves);
    app.post('/api/cve/new', Controller.addCve);
    app.post('/api/cve/delete', Controller.deleteCve);

    app.post('/api/fqdn', Controller.getFqdn);
    app.post('/api/fqdn/all', Controller.getFqdns);
    app.post('/api/fqdn/new', Controller.addFqdn);
    app.post('/api/fqdn/delete', Controller.deleteFqdn);
    app.post('/api/fqdn/update', Controller.updateFqdn);
    app.post('/api/auto', Controller.autoGetFqdn);
    app.post('/api/auto/update', Controller.autoUpdateFqdn);

    app.post('/api/url', Controller.getUrl);
    app.post('/api/url/all', Controller.getUrls);
    app.post('/api/url/new', Controller.addUrl);
    app.post('/api/url/delete', Controller.deleteUrl);
    app.post('/api/url/update', Controller.updateUrl);
    app.post('/api/url/auto', Controller.autoGetUrl);
    app.post('/api/url/auto/update', Controller.autoUpdateUrl);
    app.post('/api/url/auto/delete', Controller.autoDeleteUrl);
}