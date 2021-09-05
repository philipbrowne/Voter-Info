# Voter Info

Voter Information Application - designed to provide information on voting to US Residents based on their area in an effort to increase accessibility and engagement.

## Initial Capstone Proposal

This application is designed to provide information to voters to help increase engagement and participation. The website will provide access to location-specific information on voter registration, polling locations, voter registration deadlines. An additional component could be to provide information specific to that voter on their current registration status.

The application is designed for adults in the United States of all demographics.

I plan on using data obtained through various APIs, such as the Google Civic Information API, Rock the Vote API, the US Vote Foundation API, Vote Smart API, and the Democracy Works Elections API. I plan to keep this open ended for now until I have spent more time researching each API and what datasets are specifically available. There are quite a few directions that I could go with this as the project expands, but the MVP would be to provide location-specific voter-registration information.

The Database schema would likely contain a User profile for that specific user, an authentication component, should they want to save their data and quickly access it. I am leaving the rest of the Database Schema a bit more open ended for now until I have more information on the APIs. However, it would largely be tied to user specific information that is retrieved through this application.

As far as issues with the API, that is something I will have to explore more as I get deeper into the project. I believe that at the very least, the Google Civic Information API should be mostly reliable.

If I go in the direction of a user-login and authentication functionality, I would definitely want to keep that information secure. I would use Bcrypt hashing and any other security measures possible to achieve this.

The main core functionality of this application would be to provide area-specific information to a user on voter registration, deadlines, and their polling location. I intend to go quite a bit beyond this as time permits.

User flow would include the user entering their location and the application returning information specific to that location for the user. One consideration would definitely be to have the ability to save this information and register for the site so the user could have it readily available.

## Initial Planning

**Schema:**

My initial Schema will incorporate a single user table - I have added a screenshot of the proposed schema in my project_screenshots folder.

![](https://github.com/philipbrowne/Voter-Info/blob/main/project_screenshots/schema-v1.png?raw=true)

