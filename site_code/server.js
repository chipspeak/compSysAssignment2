const express = require('express');
const exphbs = require('express-handlebars');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Set the views directory
app.set('views', path.join(__dirname, 'views'));

// Serve static files from the views folder
app.use(express.static(path.join(__dirname, 'views')));

// Initialise handlebars as the views engine
const hbs = exphbs.create({ extname: '.handlebars', defaultLayout: 'index', layoutsDir: path.join(__dirname, 'views') });
app.engine('handlebars', hbs.engine);
app.set('view engine', 'handlebars');

app.get('/api/config', (req, res) => {
  // Load data from env file containing firebase config
  const firebaseConfig = {
    apiKey: process.env.FIREBASE_API_KEY,
    authDomain: process.env.FIREBASE_AUTH_DOMAIN,
    databaseURL: process.env.FIREBASE_DATABASE_URL,
    projectId: process.env.FIREBASE_PROJECT_ID,
    storageBucket: process.env.FIREBASE_STORAGE_BUCKET,
    messagingSenderId: process.env.FIREBASE_MESSAGING_SENDER_ID,
    appId: process.env.FIREBASE_APP_ID
  };

  res.json(firebaseConfig);
});

// Render index view
app.get('/', (req, res) => {
  res.render('index');
});
// listens for http requests
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});