import firebase_admin
from firebase_admin import credentials, firestore, storage, db
import os
from datetime import datetime

cred=credentials.Certificate('./serviceAccountKey.json')
firebase_admin.initialize_app(cred, 
                              {
                                  #'storageBucket': 'ccapi-42492.appspot.com', 
                                  'databaseURL': 'https://ccapi-42492-default-rtdb.europe-west1.firebasedatabase.app/'
                                  })

#bucket = storage.bucket()
ref = db.reference('/')
home_ref = ref.child('file')

currentTime = datetime.now()
formattedTime = currentTime.strftime("%Y-%m-%d %H:%M:%S")

'''
def store_file(fileLoc):
    filename=os.path.basename(fileLoc)
    # Store File in FB Bucket
    blob = bucket.blob(filename)
    outfile=fileLoc
    blob.upload_from_filename(outfile)
'''

def push_db(ETA, currentTime, startTime, journeyStatus):
  # Push file reference to image in Realtime DB
  home_ref.push({
      'ETA': ETA,
      'Departure Time': currentTime,
      'Start Time': startTime,
      'Journey Status': journeyStatus
      })

if __name__ == "__main__":
    '''
    f = open("./test.txt", "w")
    f.write("a demo upload file to test Firebase Storage")
    f.close()
    store_file('./test.txt')
    '''
    push_db('16:45', str(formattedTime), '17:00', 'Arriving Early')