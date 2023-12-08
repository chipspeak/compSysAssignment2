// imports
const express = require('express');
const exphbs = require('express-handlebars');
const path = require('path');

// initialising the express application and its port (or 3000 if port is undefined in the .env)
const app = express();
const PORT = 3000;

// Sets the views folder for express to the 'views' in the current folder
app.set('views', path.join(__dirname, 'views'));

// serves static files from the views folder
app.use(express.static(path.join(__dirname, 'views')));

// Initialise handlebars for rendering views and specifies extension as "handlebars" as opposed to the standard ".hbs"
// This extension change was the only way I could get the application to work
const hbs = exphbs.create({ extname: '.handlebars', defaultLayout: 'index', layoutsDir: path.join(__dirname, 'views') });

// Handlebars is set as the view engine for express
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

// Index view ('/') is rendered using handlebars
app.get('/', (req, res) => {
  res.render('index');
});

// Server listens on the PORT variable specified above (3000) and prints a message to console when it's running without issue
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
