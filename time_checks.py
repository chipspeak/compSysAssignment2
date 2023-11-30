from datetime import datetime, time, timedelta

# Create a time object
workStart = time(hour=18, minute=50)

# Combine with a datetime object with minimal date
combined_datetime = datetime.combine(datetime.min, workStart)

# subtract 10 minutes for optimal arrival time for use in main
within10 = combined_datetime - timedelta(minutes=10)
# subtract 5 minutes for optimal arrival time for use in main
within5 = combined_datetime - timedelta(minutes=5)

# Extract the time from the result and set values to be called in main
optimalArrival = within10.time()
cuttingItClose = within5.time()