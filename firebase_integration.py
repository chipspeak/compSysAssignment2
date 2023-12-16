# imports
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime

cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, 
                              { 
                                  'databaseURL': 'https://ccapi-42492-default-rtdb.europe-west1.firebasedatabase.app/'
                                  })

ref = db.reference('/')
home_ref = ref.child('file')

def push_db(currentDate, currentTime, ETA, startTime, journeyStatus):
  # Push file for realtime db
  home_ref.push({
      'Date': currentDate,
      'Departure Time': currentTime,
      'ETA': ETA,
      'Start Time': startTime,
      'Journey Status': journeyStatus
      })