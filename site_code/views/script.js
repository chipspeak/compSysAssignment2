import { initializeApp } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-app.js";
import { getDatabase, ref, get } from "https://www.gstatic.com/firebasejs/9.6.8/firebase-database.js";

const fetchConfig = async () => {
  try {
    console.log('Fetching config...');
    // Fetch Firebase config from server
    const response = await fetch('/api/config');
    const firebaseConfig = await response.json();
    console.log(firebaseConfig);

    // Initialize Firebase with the fetched config variables
    const app = initializeApp(firebaseConfig);

    // Get a reference to the firebase realtime database
    const database = getDatabase(app);

    // Reference to database (file being the name inherited from the labs)
    const dataRef = ref(database, 'file');

    // Listen for changes in the database
    get(dataRef)
      .then((snapshot) => {
        const dataList = document.getElementById('dataList');

        // Clear previous entries
        dataList.innerHTML = '';

        // Iterate over each entry in the snapshot
        snapshot.forEach((childSnapshot) => {
          const journeyData = childSnapshot.val();

          // Create a list item for each entry
          const listItem = document.createElement('li');
          listItem.textContent = `
            Date: ${journeyData.Date},
            Departure Time: ${journeyData['Departure Time']},
            ETA: ${journeyData.ETA},
            Start Time: ${journeyData['Start Time']},
            Journey Status: ${journeyData['Journey Status']}
          `;

          dataList.appendChild(listItem);
        });
      })
      .catch((error) => {
        console.error('Error getting data: ', error);
      });
  } catch (error) {
    console.error('Error fetching config:', error);
  }
};

// Call the function to initiate the fetching and setup
fetchConfig();
