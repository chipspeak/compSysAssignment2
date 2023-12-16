// imports
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, get, orderByChild, limitToLast, query } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";

// Function to fetch firebase config from the server (specifically the process.env references in server.js)
const fetchConfig = async () => {
  // try starts and renders 'Error fetching config:' below if the server communication fails
  try {
    console.log('Fetching config...');
    // the actual fetch from the config and log of this in the console
    const response = await fetch('/api/config');
    const firebaseConfig = await response.json();
    console.log(firebaseConfig);
    
    // firebase is intialised and gets a reference to the file realtime database set up in the week 11 lab
    const app = initializeApp(firebaseConfig);
    const database = getDatabase(app);
    const dataRef = ref(database, 'file');

    // query is set up to retrieve the 4 most entries in the DB by their Date using orderByChild
    // this required modification of the rules in firebase to allow for use of the Date property in ordering
    const q = query(dataRef, orderByChild('Date'), limitToLast(4));
    const snapshot = await get(q);

    // the dataContainer is retrieved and its contents are emptied (set to '')
    const dataContainer = document.getElementById('dataContainer');
    dataContainer.innerHTML = '';

    // Iterate over each entry in the snapshot and store the data from each snapshot in journeyData
    snapshot.forEach((childSnapshot) => {
      const journeyData = childSnapshot.val();

      // document.createElement is then used to create a div for each entry
      const entryContainer = document.createElement('div');
      // each container is then styled as a card class from bulma
      entryContainer.classList.add('card');

      // for of loop is used to iterate over multiple entries and their properties
      // each property is then assigned a 'p' html element which is then styled by bulma via classList.add
      for (const [key, value] of Object.entries(journeyData)) {
        const propertyElement = document.createElement('p');
        propertyElement.classList.add('p-2', 'has-text-weight-bold', 'has-text-info');
        // the content of the paragraph is then set to key and value in order to display the attribute and data from the db correctly
        propertyElement.innerHTML = `${key}: ${value}`;
        // finally the paragraph is then added to the entryContainer(bulma card)
        entryContainer.appendChild(propertyElement);
      }

      // spacing is added between entries via the creation of a horizontal rule tag and then adding that to entryContainer
      const spacingElement = document.createElement('hr');
      entryContainer.appendChild(spacingElement);

      // at this point the entry container(bulma card) and its contents are added to the dataContainer(initally created div) for use in views
      dataContainer.appendChild(entryContainer);
    });
  } catch (error) {
    console.error('Error fetching config:', error);
  }
};

// Call the function to initiate the fetching and setup
fetchConfig();