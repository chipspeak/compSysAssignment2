# compSysAssignment2

Assignment 2 for the Computer System and Networks module on the hDip in Computer Science 2023 in SETU

The Commute Chronology Assistant is a project designed to provide supports for those with poor time awareness in their daily commute.
A mixture of devices interact to allow the user to see their ETA in realtime on a sensehat display for a Rasberry Pi in addition to
ambient lighting matching the messages on a Phillips Hue Light.

There are 4 statuses based on the users current ETA relative to an optimum arrival time at their destination.

1. Status Green (user will arrive more than 10 minutes early)

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/statusgreen.gif)

2. Status Yellow (user will arrive within 5 minutes of start time)

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/statusyellow.gif)

3. Status Red (user will arrive late relative to the applications settings)

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/statusred.gif)

4. Status Blue (user has left the local network and is on their way)

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/statusblue.gif)

As long as the user's phone is detected on the local network, the google maps API will continiously be called thus providing the ETA for display.
Additionally, Blynk is incorporated in the form of phone push notifications depending on status and a realtime ETA readout widget.

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/pushnotifications.gif)

Once the user leaves, their offset(actual departure relative to desired departure) is written to a json file. The average of these offsets
is used to adjust the output to the user in an attempt to allow for their previous lateness. This effectively mimics the idea of setting
your watch 5 minutes fast. The ETA and all interactions around it are then adjusted accordingly.

Finally, in addition to the json storing departure time, ETA and offset etc, this data is also stored in a Firebase Realtime DB and displayed
on a glitch.com site. This site serves as a way to track the last 4 journeys of the user in terms of times. It also contains the installation guide
and various other links and general information.

![](https://github.com/chipspeak/compSysAssignment2/blob/main/assets/ccasite.gif)

For any other additional information, please see the installation guide and functionality diagram(both contained in the assets directory) or reach out directly.

