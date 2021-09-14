# Voter Info

![](https://github.com/philipbrowne/Voter-Info/blob/main/static/assets/images/promo-img.png)

Voter Information Application - designed to provide information on voting to US Residents based on their area in an effort to increase accessibility and engagement.

This project was completed in approximately 60 hours as part of the Springboard Software Engineering program.  

## Technologies Used

**Front End:**

JavaScript, AJAX, Axios, Bootstrap CSS

**Back End:**

Python, Flask, SQLAlchemy, WTForms, BCrypt, PyJWT, Flask Mail

**Database:**

PostgreSQL

**API and Data:**

Google Civic Information, EasyPost, MapQuest. Random Address Data from RRAD/OpenAddresses

**Graphic Design:**

Canva and Adobe Photoshop

## Deployment

The application is currently deployed on Heroku at https://us-voter-info.herokuapp.com/ 

## Features

### Registration and Login

User registration occurs through User model in SQLAlchemy and Bcrypt Hashing of their Password.  Information is stored in PostgreSQL Database.  All forms on the user end of this application are rendered and verified (CSRF) through Flask WTForms.  If a user submits a username or email already in the system, an error message is generated.

Login authentication occurs by verifying password with Bcrypt hash.

If login is successful, method returns user; if unsuccessful, it returns False.  

The user enters their mailing address, or makes a request to generate a random address, which is chosen randomly from a randAddress JS file.  The source of these addresses is [RRAD](https://github.com/EthanRBrown/rrad) and these addresses are all Public Domain through the [OpenAddresses](https://openaddresses.io/) project.  

--Register UI Screenshot--

--Login UI Screenshot--

### Address Verification Using EasyPost API

The user either uses their own address, or the randomly chosen address from randAddress.js and an AJAX request is sent to our back-end at /verify-address or /verify-random-address via POST request.  At this route, the data is sent to the [EasyPost](https://www.easypost.com/) API and verified.  If the address is verified as a real deliverable mailing address, a JSON object with the Verified Address data is returned to our Front End and handled in the DOM.  If the address is deemed undeliverable, an error is returned via JSON and the user receives a message in the DOM that the address is invalid and to try again.  I have added commented-out code in the verify-address routes that include an API call to a different Address Verification API, [Lob](https://www.lob.com/).  My experiences were better with EasyPost, but if for some reason there were issues with the API, one *further step* with this project would be to improve error handling and provide a second call to Lob if the EasyPost API is down. 

Once the address has been verified, one more API request goes out quickly to the [Mapquest](https://developer.mapquest.com/) API to retrieve the user's county based on their address to add it to the User Profile.

--Register UI Screenshot 2--

### Password Reset

Change Password is handled via a Password Reset process through JWT and Flask Mail. 

A user requests a password via Flask View with their previously supplied Email Address.  Flask Mail emails the user at the provided address with a Password Reset Link.  The URL in this link includes a JWT Token at the end of the URL.  

At that URL, a user can fill out a very short form to reset their password.

--Password Reset UI Screenshot--

### User Profile

Upon registration and login, the application takes the user to their profile, where they can see their user information, as well as pertinent voting information based on their state.  The user can edit their profile, where a form similar to registration appears with all details except their Username and/or Password.

--User Profile UI Screenshot--

--Edit User UI Screenshot--

### Public Officials

Data for Public Officials is generated via the user's address and the [Google Civic Information](https://developers.google.com/civic-information) API.  A response contains three main items of organization: division (the level of government), office (the office of the official), and official (the elected official).  I have provided three screenshot examples here:

[Google Civic Info Screenshots]

I created multiple images for various public offices using Canva Graphic Design tools and I ran a Jinja loop through the offices and officials.  I then created a conditional through Jinja templating to evaluate which office the iteration is currently on.  

[Public Officials Screenshots]

### **Elections**

I was able to retrieve extremely limited data from Google Civic Information API on upcoming elections.  At the time of first deployment, there were only seven elections being returned for the entire country, one of them occurring on September 14 in California.  I have included any election data available for a user's address from the API (users in California would be able to see this information at the time of first launch), but most users would not receive anything.

I made fairly extensive effort to locate this data in other free Election APIs, however I was unsuccessful in locating anything that would be particularly helpful.  However, after initiating contact with their support team, I was informed that [CivicsEngine](https://www.civicengine.com/) is currently in the process of creating a free API in the future.  I believe that their data could be extremely valuable to developers.

Because of this lack of information, I decided that the best thing to do for this present project was to create a new database of information containing upcoming elections, which I have included in my Database Seed file in the main folder.  I gathered this information from each state using various public resources including each state's Board of Elections website.  Of course, this information will become outdated fairly quickly, and it would be much better practice in development to fetch this data from an API that is constantly updating its information.  Unfortunately, that was not an option at the time of developing this application.  I am looking forward to seeing what data CivicsEngine releases publicly with their API and based on that data, I would definitely consider improving my application to retrieve the data in a more dynamic manner.  I have also included a link to the respective state's Board of Elections website where they can find more information on future elections.

I've attempted to provide an easy way to update this information for Admin users in the Admin section of my application.

[Screenshot State Elections UI]

### State Voting Information

Unfortunately, at the time of release, I was unable to locate any free and public API that provided Registration/Voting information and data based on the user's location.  

Similarly to the Elections section of the application, I decided that the best alternative was to create a new database on my application and manually seed the data.  

Due to the fact that there are so many columns on this table, I felt that it would be best to quickly go through each of them from the State Database model.

**ID:** Primary Key - State Abbreviation (i.e. 'AL' for Alabama)

**name:** Name of state (i.e. Alabama)

**capital:** State Capital (i.e. Montgomery)

**registration_url:** URL from State Board of Elections for Voter Registration

**elections_url:** Upcoming Elections URL from State Board of Elections for Upcoming Elections

**Deadlines for Voter Registration:**

**registration_in_person_deadline:** Deadline for Voter Registration in person

**registration_mail_deadline:** Deadline for Voter Registration by mail

**registration_online_deadline:** Deadline for Voter Registration online

**Deadlines for Absentee Ballot Application and Voting:**

**absentee_application_in_person_deadline:** Deadline to apply for Absentee Ballot in person

**absentee_application_mail_deadline:** Deadline to apply for Absentee Ballot by mail

**absentee_application_online_deadline:** Deadline to apply for Absentee Ballot online

**voted_absentee_ballot_deadline:** Due date for Absentee Ballot

**check_registration_url:** URL on State website to check voter's registration status

**polling_location_url:** URL on State website to check a voter's polling location

**absentee_ballot_url:**URL on State website to apply for Absentee Ballot

**local_election_url:** URL on State website to locate location election board/clerks/etc

**ballot_tracker_url:** URL on State website to check track ballot location

I gathered this information from various sources, including the State Board of Elections websites and included it in my seed.py file.

**Voter Registration Rules**

I created a separate database table for Voter Registration rules.  I gathered this information from public data for each state and added it to my database.  There were very few specific rules that overlapped between states, with the main exception of "You must be a citizen of the United States".  However, I wanted to provide flexibility for any rules that were in multiple states, so I handled this with a StateRegistrationRule join table.

I've attempted to provide an easy way to update this information for Admin users in the Admin section of my application.

At the bottom of the State Voting Information section, I have included information from the Google Civic Information API pertaining to the user's state officials, based on that specific division in the JSON data.

Screenshots for State Voting Info

## Further Steps

