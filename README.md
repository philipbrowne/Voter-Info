# Voter Info

![](https://us-voter-info.herokuapp.com/assets/promo-img/site-promo-img.png)

Voter Info - designed to provide information on voting to US Residents based on their area in an effort to increase accessibility and engagement.

This project was completed in approximately 50-60 hours as part of the Springboard Software Engineering fellowship program.

# Table of Contents
1. [Technologies Used](##Technologies Used)
2. [Front End](####Front End)
3. [Back End](####Back End)
4. [Database](####Database)
5. [API and Data](####API and Data)
6. [Graphic Design](####Graphic Design)

## Technologies Used

#### Front End:

JavaScript, AJAX, Axios, Bootstrap CSS

#### Back End:

Python, Flask, SQLAlchemy, WTForms, BCrypt, PyJWT, Flask Mail

#### Database:

PostgreSQL

#### API and Data:

Google Civic Information, EasyPost (alternative request using Lob included as commented code in app file), MapQuest. Random Address Data from RRAD/OpenAddresses

#### Graphic Design:

Canva and Adobe Photoshop

## Deployment

The application is currently deployed on Heroku at https://us-voter-info.herokuapp.com/

## Developer

**[Phil Browne](https://www.linkedin.com/in/philbrownetech/)**

![](https://us-voter-info.herokuapp.com/assets/images/phil.jpg)

**Email:** pbrowne@gmail.com

## Video Demo

**Video Demo of the application:** https://us-voter-info.herokuapp.com/assets/video/Voter-Info-Demo.mp4

## Demo Account For Site Use

This application uses User Registration and Login. However, if you do not wish to register for an account, you can sign in as a TestUser under the credentials below:

Username: TestUser
Password: TestPassword!

## Features

### Registration and Login

User registration occurs through User model in SQLAlchemy and Bcrypt Hashing of their Password. Information is stored in PostgreSQL Database. All forms on the user end of this application are rendered and verified (CSRF) through Flask WTForms. If a user submits a username or email already in the system, an error message is generated.

Login authentication occurs by verifying password with Bcrypt hash.

If login is successful, method returns user; if unsuccessful, it returns False.

The user enters their mailing address, or makes a request to generate a random address, which is chosen randomly from a randAddress JS file. The source of these addresses is [RRAD](https://github.com/EthanRBrown/rrad) and these addresses are all Public Domain through the [OpenAddresses](https://openaddresses.io/) project.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/user-registration-ui-screenshot2.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/user-login-ui-screenshot.png?raw=true)

### Address Verification Using EasyPost API

The user either uses their own address, or the randomly chosen address from randAddress.js and an AJAX request is sent to our back-end at /verify-address or /verify-random-address via POST request. At this route, the data is sent to the [EasyPost](https://www.easypost.com/) API and verified. If the address is verified as a real deliverable mailing address, a JSON object with the Verified Address data is returned to our Front End and handled in the DOM. If the address is deemed undeliverable, an error is returned via JSON and the user receives a message in the DOM that the address is invalid and to try again. I have added commented-out code in the verify-address routes that include an API call to a different Address Verification API, [Lob](https://www.lob.com/). My experiences were better with EasyPost, but if for some reason there were issues with the API, one _further step_ with this project would be to improve error handling and provide a second call to Lob if the EasyPost API is down.

Once the address has been verified, one more API request goes out quickly to the [Mapquest](https://developer.mapquest.com/) API to retrieve the user's county based on their address to add it to the User Profile.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/user-registration-ui-screenshot1.png?raw=true)

### Password Reset

Change Password is handled via a Password Reset process through JWT and Flask Mail.

A user requests a password via Flask View with their previously supplied Email Address. Flask Mail emails the user at the provided address with a Password Reset Link. The URL in this link includes a JWT Token at the end of the URL.

At that URL, a user can fill out a very short form to reset their password.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/user-reset-password-ui-screenshot.png?raw=true)

### User Profile

Upon registration and login, the application takes the user to their profile, where they can see their user information, as well as pertinent voting information based on their state. The user can edit their profile, where a form similar to registration appears with all details except their Username and/or Password.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/user-profile-ui-screenshot.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/edit-user-ui-screenshot.png?raw=true)

### Public Officials

Data for Public Officials is generated via the user's address and the [Google Civic Information](https://developers.google.com/civic-information) API. A response contains three main items of organization: division (the level of government), office (the office of the official), and official (the elected official). I have provided three screenshot examples here:

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/google-civic-information-screenshot-1.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/google-civic-information-screenshot-2.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/google-civic-information-screenshot-3.png?raw=true)

I created multiple images for various public offices using Canva Graphic Design tools and I ran a Jinja loop through the offices and officials. I then created a conditional through Jinja templating to evaluate which office the iteration is currently on.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/public-officials-screenshot-1.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/public-officials-screenshot-2.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/public-officials-screenshot-3.png?raw=true)

### Elections

I was able to retrieve extremely limited data from Google Civic Information API on upcoming elections. At the time of first deployment, there were only seven elections being returned for the entire country, one of them occurring on September 14 in California. I have included any election data available for a user's address from the API (users in California would be able to see this information at the time of first launch), but most users would not receive anything.

I made fairly extensive effort to locate this data in other free Election APIs, however I was unsuccessful in locating anything that would be particularly helpful. However, after initiating contact with their support team, I was informed that [CivicsEngine](https://www.civicengine.com/) is currently in the process of creating a free API in the future. I believe that their data could be extremely valuable to developers.

Because of this lack of information, I decided that the best thing to do for this present project was to create a new database of information containing upcoming elections, which I have included in my Database Seed file in the main folder. I gathered this information from each state using various public resources including each state's Board of Elections website. Of course, this information will become outdated fairly quickly, and it would be much better practice in development to fetch this data from an API that is constantly updating its information. Unfortunately, that was not an option at the time of developing this application. I am looking forward to seeing what data CivicsEngine releases publicly with their API and based on that data, I would definitely consider improving my application to retrieve the data in a more dynamic manner. I have also included a link to the respective state's Board of Elections website where they can find more information on future elections.

I've attempted to provide an easy way to update this information for Admin users in the Admin section of my application.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/state-elections-ui-screenshot.png?raw=true)

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

I created a separate database table for Voter Registration rules. I gathered this information from public data for each state and added it to my database. There were very few specific rules that overlapped between states, with the main exception of "You must be a citizen of the United States". However, I wanted to provide flexibility for any rules that were in multiple states, so I handled this with a StateRegistrationRule join table.

I've attempted to provide an easy way to update this information for Admin users in the Admin section of my application.

At the bottom of the State Voting Information section, I have included information from the Google Civic Information API pertaining to the user's state officials, based on that specific division in the JSON data.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/state-voting-info-ui-screenshot-1.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/state-voting-info-ui-screenshot-2.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/state-voting-info-ui-screenshot-3.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/state-voting-info-ui-screenshot-4.png?raw=true)

### Administrator Interface

Due to the amount of data that was manually added, and for long-term sustainability of this application, I decided that it was best to add an Administrator interface to the application. Each user has a Boolean value in the User model for "is_admin" that defaults to false upon registration. However, if a user does have the value set to True, they will have access to this administrator interface, where they can create, read, update, and delete data from our system. In my current Deployment, I assigned is_admin to my own user profile using Heroku's PostgreSQL interface, this can also be done similarly in local deployments.

##### Admin Main Page:

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-1.png?raw=true)

##### Admin - Users:

The Administrator can edit most of a user's details, with the exception of the password, which the user can only change themselves through the Password Reset functionality described above.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-2.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-3.png?raw=true)

The Administrator can also add administrative authorization to the user.

##### Admin - States:

The Administrator can edit state information - adding/removing rules, adding elections, etc.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-4.png?raw=true)

![[Admin-Page-UI-5]](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-5.png?raw=true)

##### Admin - Elections:

The Administrator can add, edit, and remove elections.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-6.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-7.png?raw=true)

##### Admin: Voter Registration Rules:

The Administrator can add, edit, and remove voter registration rules.

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-8.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-9.png?raw=true)

![](https://github.com/philipbrowne/us-voter-info/blob/main/project_screenshots/admin-page-ui-10.png?raw=true)

## Further Steps

##### Data Models:

As mentioned, the situation with our State Voter Information and State Elections data is less than ideal. I intend to continue looking for a free and public API that will provide this information. It is my hope that the Administrator functionality will help at least partially offset this deficiency.

There are many other voter information items that would be valuable, such as Absentee Voting Rules, Voter ID Rules, Early Voting Dates, Election Day Registration, etc. Unfortunately, within the time allowed for this project, I was not able to add additional information. However, these are definitely further items I would consider adding to my State data model.

##### Additional Functionality:

Setting an Email reminder system for voting based on the election date would definitely be an added function that I would like to implement in the future. Alternatively, I could add text Reminders using the [Twilio](https://www.twilio.com/docs/usage/api) API, but would have to do it in a way that is non-invasive to the user. A reminder to the user if they are under the age of 18 to register when eligible could also be helpful.

##### Improved Error Handling for APIs

With more time, I would definitely improve my error handling if an API were to go down, particularly the EasyPost API. I've commented out the Lob API call as a backup option, and intend to explore ways I could alternatively use that if EasyPost was ever to go down.

All feedback is appreciated - please feel free to connect with me using the information listed under "Developer".

## Local Deployment

###### Requirements:

Python, Pip, PostgreSQL

###### API Keys and Email:

Retrieve free API keys for Lob, EasyPost, Google Civic Information, and Mapquest; substitute them in the variables I have listed in app.py. For email functionality, substitute with a gmail account of your own choosing with the MAIL_USERNAME and MAIL_PASSWORD variables in my app file. For the SECRET_KEY variable in Flask, you can use your own variable locally.

###### To deploy locally using Python 3.711, pip, and Flask:

Initialize PostgreSQL in your operating system and run the following commands in your terminal:

###### Clone Repository and Enter Directory of Repo

`git clone https://github.com/philipbrowne/us-voter-info`

`cd us-voter-info`

###### Create and Activate Python Virtual Environment

`python3.7 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

###### To Set Up Our Local Database:

`createdb voter-db`

`python3.7 seed.py`

###### Run Application With Flask

`export FLASK_ENV=production`

`export FLASK_RUN_PORT=8000`

`flask run`

Open the application in your web browser at http://localhost:8000/
