# Voter Info

![](https://github.com/philipbrowne/Voter-Info/blob/main/static/assets/images/promo-img.png)

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

It is very likely that more tables will be added to this project as this project gets more complex, but I believe that the basic application should be able to properly operate with this single table of data for now.

**Update (9/7): Second Table Added:**
![](https://github.com/philipbrowne/Voter-Info/blob/main/project_screenshots/schema-v2.png)

Update(9/8) Third Table Added for Registration Rules, as well as Join Table between States/Registration Rules



I have added a second table for State which I will incorporate various important state-specific details such as voter registration URL, elections schedule URL, etc.  I will add more columns to this table over time.

**API Links for Project**

I am planning to use multiple APIs for this project. Several of the proposed ones are below, I will review documentation for each and proceed based on which will be the most useful. Once I have achieved an Minimum Viable Product for the application, I will begin to implement additional features and add them using the APIs below.

Lob API for Address Verification: https://docs.lob.com/python -- Using for User Registration to Verify Address

Random Address File from RRAD: https://github.com/EthanRBrown/rrad - Using to Generate Random User Mailing Address

Associated Press Elections API: https://developer.ap.org/ap-elections-api/

Mapquest API for any necessary geocoding of user location: https://developer.mapquest.com/documentation/

Google Civic Information API: https://developers.google.com/civic-information

RockTheVote API (will be useful for assisting with Voter Registration): https://rock-the-vote.github.io/Voter-Registration-Tool-API-Docs/#overview

US Vote Foundation API: https://civicdata.usvotefoundation.org/

Democracy Works Elections API: https://www.democracy.works/elections-api

VoteSmart API: https://votesmart.org/share/api

Elections Online API: https://www.electionsonline.com/integrations/api.cfm

WeVoteUSA API: https://api.wevoteusa.org/apis/v1/docs/

Voting Information Project API: https://vip-specification.readthedocs.io/en/release/index.html

CivicEngine API: https://developers.civicengine.com/docs/api/v1

## Project Screenshots

**Representatives Page for User based on their Address**

![](https://github.com/philipbrowne/Voter-Info/blob/main/project_screenshots/representatives-v1.png)

