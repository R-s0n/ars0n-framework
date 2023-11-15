const mongoose = require('mongoose');

const mongoHost = process.env.MONGO_HOST || '0.0.0.0'
const dbName = process.env.DB_NAME || 'wapt_db';

mongoose.connect(`mongodb://${mongoHost}/${dbName}`, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(()=>console.log("Database connection established..."))
    .catch(err=>console.log("ERROR: ", err));