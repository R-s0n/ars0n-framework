const mongoose = require('mongoose');
const dotenv = require('dotenv');

dotenv.config();

mongoose.connect(`mongodb://${process.env.HOST || '127.0.0.1'}/wapt_db`, {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(()=>console.log("Database connection established..."))
    .catch(err=>console.log("ERROR: ", err));