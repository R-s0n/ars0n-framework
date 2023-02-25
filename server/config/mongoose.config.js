const mongoose = require('mongoose');

mongoose.connect('mongodb://localhost/ars0n_framework_db', {
    useNewUrlParser: true,
    useUnifiedTopology: true
})
    .then(()=>console.log("Database connection established..."))
    .catch(err=>console.log("ERROR: ", err));