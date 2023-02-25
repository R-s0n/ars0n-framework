const express = require('express');
const app = express();
const cors = require('cors');
const port = 8000;
const bodyParser = require('body-parser');

app.use(cors());
app.use(express.urlencoded({extended: true}))
app.use(bodyParser.json({limit: '50mb'}));
app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

require('./config/mongoose.config');

require('./routes/Routes.js')(app);

app.listen(port, () => console.log(`Listening on port: ${port}`) );