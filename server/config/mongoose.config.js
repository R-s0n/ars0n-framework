const mongoose = require('mongoose');

mongoose.connect('mongodb://127.0.0.1/wapt_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(()=>console.log("Database connection established..."))
    .catch(err=>console.log("ERROR: ", err));