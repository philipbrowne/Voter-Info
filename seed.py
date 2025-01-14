from requests.models import REDIRECT_STATI
from models import RegistrationRule, StateRegistrationRule, db, State, User, Election
from app import app

db.drop_all()
db.create_all()

#Data for Each State - Please see http://www.github.com/philipbrowne/us-voter-info for more information

AL = State(id='AL', name='Alabama', capital='Montgomery', registration_url='https://www.sos.alabama.gov/alabama-votes/voter/register-to-vote?ref=voteusa',
           elections_url='https://www.sos.alabama.gov/alabama-votes/voter/upcoming-elections', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://myinfo.alabamavotes.gov/VoterView/RegistrantSearch.do', polling_location_url='https://myinfo.alabamavotes.gov/VoterView/PollingPlaceSearch.do', absentee_ballot_url='https://www.sos.alabama.gov/alabama-votes/voter/absentee-voting', local_election_url='https://sos.alabama.gov/city-county-lookup&sa=D&source=editors&ust=1631123483717000&usg=AOvVaw3wN0m7RnMeBdnN1l8i21aU', ballot_tracker_url='https://myinfo.alabamavotes.gov/VoterView/AbsenteeBallotSearch.do', absentee_application_in_person_deadline='Received 5 days before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked 1 day before Election Day, received by noon on Election Day.')
AK = State(id='AK', name='Alaska', capital='Juneau', registration_url='https://www.elections.alaska.gov/Core/voterregistration.php',
           elections_url='https://www.elections.alaska.gov/Core/generalelectioninformation.php', registration_in_person_deadline='30 days before Election Day.', registration_mail_deadline='Postmarked at least 30 days before Election Day.', registration_online_deadline='30 days before Election Day.', check_registration_url='https://myvoterinformation.alaska.gov/', polling_location_url='https://myvoterinformation.alaska.gov/', absentee_ballot_url='https://elections.alaska.gov/Core/AKVoteEarly.php', local_election_url='http://www.elections.alaska.gov/Core/contactregionalelectionsoffices.php%23bkR1&sa=D&source=editors&ust=1631123483717000&usg=AOvVaw1vcnJ3dqlJo-C6L-8OejqD', ballot_tracker_url='https://myvoterinformation.alaska.gov/', absentee_application_in_person_deadline='Received 10 days before Election Day.', absentee_application_mail_deadline='Received 10 days before Election Day.', absentee_application_online_deadline='Received 10 days before Election Day.', voted_absentee_ballot_deadline='Postmarked by Election Day and received 10 days after Election Day.')
AZ = State(id='AZ', name='Arizona', capital='Phoenix', registration_url='https://azsos.gov/elections/voting-election/register-vote-or-update-your-current-voter-information',
           elections_url='https://azsos.gov/elections/elections-calendar-upcoming-events', registration_in_person_deadline='29 days before Election Day, or on the next immediate business day if the deadline falls on a legal holiday or weekend.', registration_mail_deadline='Postmarked 29 days before Election Day, or on the next immediate business day if the deadline falls on a legal holiday or weekend.', registration_online_deadline='29 days before Election Day.', check_registration_url='https://my.arizona.vote/PortalList.aspx', polling_location_url='https://voter.azsos.gov/VoterView/PollingPlaceSearch.do', absentee_ballot_url='https://azsos.gov/votebymail', local_election_url='https://azsos.gov/elections/voting-election/contact-information-county-election-officials&sa=D&source=editors&ust=1631123483717000&usg=AOvVaw354iiJbiDgylGSXTVQBzNJ', ballot_tracker_url='https://my.arizona.vote/PortalList.aspx', absentee_application_in_person_deadline='Received 11 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='Received 11 days before Election Day.', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
AR = State(id='AR', name='Arkansas', capital='Little Rock',
           registration_url='https://www.sos.arkansas.gov/elections/for-voters', elections_url='https://www.sos.arkansas.gov/elections', registration_in_person_deadline='30 days before Election Day. If this falls on a Saturday, Sunday, or legal holiday, then on the next day which is not a Saturday, Sunday, or legal holiday.', registration_mail_deadline='Postmarked 30 days before Election Day. If this falls on a Saturday, Sunday, or legal holiday, then on the next day which is not a Saturday, Sunday, or legal holiday.', registration_online_deadline='N/A', check_registration_url='https://www.voterview.ar-nova.org/voterview', polling_location_url='https://www.voterview.ar-nova.org/voterview', absentee_ballot_url='https://www.sos.arkansas.gov/elections/voter-information/absentee-voting', local_election_url='https://www.sos.arkansas.gov/uploads/elections/Arkansas%2520County%2520Clerks%2520-%2520Revised%2520September%25202016.pdf&sa=D&source=editors&ust=1631123483717000&usg=AOvVaw0qXScCuyUGNfKQhT4iIG2g', ballot_tracker_url='https://www.voterview.ar-nova.org/voterview', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='In Person: Received by COB the day before Election Day. By Mail: Received by 7:30pm on Election Day.')
CA = State(id='CA', name='California', capital='Sacramento',
           registration_url='https://registertovote.ca.gov/', elections_url='https://www.sos.ca.gov/elections', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://www.sos.ca.gov/elections/registration-status/', polling_location_url='http://www.sos.ca.gov/elections/polling-place/', absentee_ballot_url='https://www.sos.ca.gov/elections/voter-registration/vote-mail', local_election_url='https://www.sos.ca.gov/elections/voting-resources/county-elections-offices/', ballot_tracker_url='https://www.sos.ca.gov/elections/ballot-status/', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received no later than 17 days after the Election.')
CO = State(id='CO', name='Colorado', capital='Denver', registration_url='https://www.sos.state.co.us/voter/pages/pub/olvr/verifyNewVoter.xhtml',
           elections_url='https://www.sos.state.co.us/pubs/elections/electionInfo.html', registration_in_person_deadline='Election Day.', registration_mail_deadline='Received 8 days before Election Day.', registration_online_deadline='8 days before Election Day.', check_registration_url='https://www.sos.state.co.us/voter/pages/pub/olvr/findVoterReg.xhtml', polling_location_url='https://www.sos.state.co.us/voter-classic/pages/pub/olvr/findVoterReg.xhtml', absentee_ballot_url='https://www.sos.state.co.us/pubs/elections/UOCAVA.html', local_election_url='https://www.sos.state.co.us/pubs/elections/Resources/CountyElectionOffices.html', ballot_tracker_url='https://colorado.ballottrax.net/voter/', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 8 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
CT = State(id='CT', name='Connecticut', capital='Hartford', registration_url='https://voterregistration.ct.gov/OLVR/welcome.do',
           elections_url='https://portal.ct.gov/SOTS/Election-Services/Calendars/Election-Calendars', registration_in_person_deadline='Note: Connecticut also has Election Day Registration on Election Day.', registration_mail_deadline='Postmarked or received 7 days before Election Day.', registration_online_deadline='7 days before Election Day.', check_registration_url='https://portaldir.ct.gov/sots/LookUp.aspx', polling_location_url='https://portal.ct.gov/SOTS/Election-Services/Voter-Information/Where-and-how-do-I-vote', absentee_ballot_url='https://portal.ct.gov/SOTS/Election-Services/Voter-Information/Absentee-Voting', local_election_url='https://portal.ct.gov/SOTS/Election-Services/Find-Your-Town-Clerk-Registrar-and-Elected-Officials/Find-Your-Town-Clerk-Registrar-of-Voters-and-Elected-Officials', ballot_tracker_url='https://portaldir.ct.gov/sots/LookUp.aspx', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='Received 1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day.')
DE = State(id='DE', name='Delaware', capital='Dover', registration_url='https://ivote.de.gov/VoterView',
           elections_url='https://elections.delaware.gov/calendars.shtml', registration_in_person_deadline='The fourth Saturday before Election Day.', registration_mail_deadline='Postmarked by the fourth Saturday before Election Day.', registration_online_deadline='The fourth Saturday before Election Day.', check_registration_url='https://ivote.de.gov/voterview', polling_location_url='https://ivote.de.gov/voterlogin.aspx', absentee_ballot_url='https://ivote.de.gov/VoterView', local_election_url='https://elections.delaware.gov/locations.shtml', ballot_tracker_url='https://ivote.de.gov/VoterView', absentee_application_in_person_deadline='Received 4 days before Election Day.', absentee_application_mail_deadline='Received 4 days before Election Day.', absentee_application_online_deadline='Received 4 days before Election Day.', voted_absentee_ballot_deadline='Received Election Day.')
DC = State(id='DC', name='District of Columbia', capital='District of Columbia',
           registration_url='https://www.dcboe.org/Voters/Register-To-Vote/Register-to-Vote', elections_url='https://dcboe.org/Community-Outreach/Events', registration_in_person_deadline='If you submit your application in person at the Board of Elections or another voter registration agency, your application should be received no later than the day before the start of the early voting period. OR If you miss the deadline, Same-Day Registration is available during Early Voting and on Election Day, with proof of residency.', registration_mail_deadline='Received 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://www.dcboe.org/Voters/Register-To-Vote/Check-Voter-Registration-Status', polling_location_url='https://www.vote4dc.com/SearchElection/SearchByAddress', absentee_ballot_url='https://www.dcboe.org/Voters/Absentee-Voting/Request-an-Absentee-Ballot', local_election_url='https://www.dcboe.org/', ballot_tracker_url='https://www.dcboe.org/Voters/Absentee-Voting/Track-Absentee-Ballot', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='Received 7 days before Election Day.', voted_absentee_ballot_deadline='Postmarked on or before Election Day and received no later than 10 days after Election Day.')
FL = State(id='FL', name='Florida', capital='Tallahassee', registration_url='https://registertovoteflorida.gov/home',
           elections_url='https://dos.myflorida.com/elections/for-voters/election-dates/', registration_in_person_deadline='29 days before Election Day.', registration_mail_deadline='Postmarked 29 days before Election Day.', registration_online_deadline='29 days before Election Day.', check_registration_url='http://registration.elections.myflorida.com/CheckVoterStatus', polling_location_url='https://registration.elections.myflorida.com/CheckVoterStatus', absentee_ballot_url='https://www.dos.myflorida.com/elections/for-voters/voting/vote-by-mail/', local_election_url='https://dos.myflorida.com/elections/contacts/supervisor-of-elections/', ballot_tracker_url='https://dos.myflorida.com/elections/for-voters/check-your-voter-status-and-polling-place/ballot-information-and-status-lookup/', absentee_application_in_person_deadline='Received 10 days before Election Day.', absentee_application_mail_deadline='Received 10 days before Election Day.', absentee_application_online_deadline='Received 10 days before Election Day.', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
GA = State(id='GA', name='Georgia', capital='Atlanta', registration_url='https://georgia.gov/register-to-vote',
           elections_url='https://sos.ga.gov/index.php/elections/elections_and_voter_registration_calendars', registration_in_person_deadline='The fifth Monday before Election Day.', registration_mail_deadline='Postmarked the fifth Monday before Election Day.', registration_online_deadline='The fifth Monday before Election Day.', check_registration_url='https://www.mvp.sos.ga.gov/MVP/mvp.do', polling_location_url='https://www.mvp.sos.ga.gov/MVP/mvp.do', absentee_ballot_url='https://georgia.gov/vote-absentee-ballot', local_election_url='https://elections.sos.ga.gov/Elections/countyelectionoffices.do', ballot_tracker_url='https://www.mvp.sos.ga.gov/MVP/mvp.do', absentee_application_in_person_deadline='Received 11 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='Received 11 days before Election Day.', voted_absentee_ballot_deadline='Received by the time the polls close on Election Day.')
HI = State(id='HI', name='Hawaii', capital='Honolulu', registration_url='https://elections.hawaii.gov/register-to-vote/registration/',
           elections_url='https://elections.hawaii.gov/voting/contest-schedule/', registration_in_person_deadline='30 days before Election Day, extended to the next business day if this falls on a Sunday.', registration_mail_deadline='Postmarked 30 days before Election Day, extended to the next business day if this falls on a Sunday.', registration_online_deadline='30 days before Election Day, extended to the next business day if this falls on a Sunday.', check_registration_url='https://olvr.hawaii.gov/register.aspx', polling_location_url='https://olvr.hawaii.gov/', absentee_ballot_url='https://electionsdev80.hawaii.gov/voters/absentee-voting/', local_election_url='https://elections.hawaii.gov/resources/county-election-divisions/', ballot_tracker_url='https://ballotstatus.hawaii.gov/Default', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
ID = State(id='ID', name='Idaho', capital='Boise', registration_url='https://elections.sos.idaho.gov/ElectionLink/ElectionLink/ApplicationInstructions.aspx',
           elections_url='https://sos.idaho.gov/elections-division/calendars/', registration_in_person_deadline='25 days before Election Day. If you miss this deadline, you may also register on Election Day. (You must show proof of residence to register at the poll.)', registration_mail_deadline='Postmarked 25 days before Election Day.', registration_online_deadline='25 days before Election Day.', check_registration_url='https://elections.sos.idaho.gov/ElectionLink/ElectionLink/VoterSearch.aspx', polling_location_url='https://apps.idahovotes.gov/YourPollingPlace/WhereDoIVote.aspx', absentee_ballot_url='https://elections.sos.idaho.gov/ElectionLink/ElectionLink/BeginAbsenteeRequest.aspx', local_election_url='https://voteidaho.gov/', ballot_tracker_url='https://idahovotes.gov/online-voter-tools/', absentee_application_in_person_deadline='Received 11 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='Received 11 days before Election Day.', voted_absentee_ballot_deadline='Received by 8pm Election Day.')
IL = State(id='IL', name='Illinois', capital='Springfield', registration_url='https://ova.elections.il.gov/?Name=Em5DYCKC4wXCKQSXTgsQ9knm%2b5Ip27VC&T=637623864062530637',
           elections_url='https://www.elections.il.gov/Main/CalendarEventsAll.aspx?T=637665305487546022', registration_in_person_deadline='28 days before Election Day, after which you may register during the early voting period through Election Day.', registration_mail_deadline='Postmarked 28 days before Election Day.', registration_online_deadline='16 days before Election Day.', check_registration_url='https://ova.elections.il.gov/RegistrationLookup.aspx', polling_location_url='https://ova.elections.il.gov/RegistrationLookup.aspx', absentee_ballot_url='https://www.elections.il.gov/ElectionOperations/VotingByMailAgreement.aspx?T=637623864274160862', local_election_url='https://elections.il.gov/electionoperations/electionauthorities.aspx', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 5 days before Election Day.', absentee_application_online_deadline='Received 5 days before Election Day.', voted_absentee_ballot_deadline='Postmarked by Election Day and received by 14 days after Election Day.')
IN = State(id='IN', name='Indiana', capital='Indianapolis', registration_url='https://www.in.gov/sos/elections/voter-information/register-to-vote/',
           elections_url='https://www.in.gov/sos/elections/voter-information/', registration_in_person_deadline='29 days before Election Day.', registration_mail_deadline='Postmarked 29 days before Election Day.', registration_online_deadline='29 days before Election Day.', check_registration_url='https://indianavoters.in.gov/', polling_location_url='https://indianavoters.in.gov/', absentee_ballot_url='https://www.in.gov/sos/elections/voter-information/ways-to-vote/absentee-voting/', local_election_url='https://indianavoters.in.gov/CountyContact/index', ballot_tracker_url='https://indianavoters.in.gov/', absentee_application_in_person_deadline='Received 12 days before Election Day.', absentee_application_mail_deadline='Received 12 days before Election Day.', absentee_application_online_deadline='Received 12 days before Election Day.')
IA = State(id='IA', name='Iowa', capital='Des Moines', registration_url='https://sos.iowa.gov/elections/voterinformation/voterregistration.html',
           elections_url='https://sos.iowa.gov/elections/electioninfo/3yrelectioncal.html', registration_in_person_deadline='15 days before Election Day. If you miss the deadline, you can also register to vote in-person during early vote or on Election Day.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://sos.iowa.gov/elections/VoterReg/RegToVote/search.aspx', polling_location_url='https://sos.iowa.gov/elections/voterreg/pollingplace/search.aspx', absentee_ballot_url='https://sos.iowa.gov/elections/electioninfo/absenteeinfo.html', local_election_url='https://sos.iowa.gov/elections/auditors/auditorslist.html', ballot_tracker_url='https://sos.iowa.gov/elections/absenteeballotstatus/absentee/search', absentee_application_in_person_deadline='Received 1 day before Election Day unless the polls open at noon. If the polls open at noon, you may cast an absentee ballot at the county auditor\'s office from 8am to 11am on Election Day.', absentee_application_mail_deadline='Received 15 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received before close of polls on Election Day.')
KS = State(id='KS', name='Kansas', capital='Topeka', registration_url='https://www.kdor.ks.gov/Apps/VoterReg/Default.aspx',
           elections_url='https://www.sos.ks.gov/elections/elections.html', registration_in_person_deadline='21 days before Election Day.', registration_mail_deadline='Postmarked 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://myvoteinfo.voteks.org/VoterView/RegistrantSearch.do', polling_location_url='https://myvoteinfo.voteks.org/VoterView/PollingPlaceSearch.do', absentee_ballot_url='https://sos.ks.gov/elections/voter-information.html', local_election_url='https://www.sos.ks.gov/elections/county_election_officers.aspx', ballot_tracker_url='https://myvoteinfo.voteks.org/voterview/', absentee_application_in_person_deadline='Received 7 days before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received 3 days after Election Day.')
KY = State(id='KY', name='Kentucky', capital='Frankfort',
           registration_url='https://fj.usembassy.gov/u-s-citizen-services/voting/', elections_url='https://elect.ky.gov/Resources/Pages/Election-Calendar.aspx', registration_in_person_deadline='29 days before Election Day.', registration_mail_deadline='Postmarked 29 days before Election Day.', registration_online_deadline='29 days before Election Day.', check_registration_url='https://vrsws.sos.ky.gov/VIC/', polling_location_url='https://vrsws.sos.ky.gov/vic/', absentee_ballot_url='https://elect.ky.gov/Frequently-Asked-Questions/Pages/Absentee-Voting.aspx', local_election_url='https://elect.ky.gov/About-Us/Pages/County-Boards-of-Elections.aspx', ballot_tracker_url='https://vrsws.sos.ky.gov/VIC/', absentee_application_in_person_deadline='7 days before Election Day', absentee_application_mail_deadline='7 days before Election Day', absentee_application_online_deadline='Received 25 days before Election Day.', voted_absentee_ballot_deadline='Received by 6pm Election Day.')
LA = State(id='LA', name='Louisiana', capital='Baton Rouge', registration_url='https://www.sos.la.gov/ElectionsAndVoting/RegisterToVote/Pages/default.aspx',
           elections_url='https://www.sos.la.gov/ElectionsAndVoting/GetElectionInformation/SearchElectionDates/Pages/default.aspx', registration_in_person_deadline='30 days before Election Day.', registration_mail_deadline='Postmarked 30 days before Election Day.', registration_online_deadline='20 days before Election Day.', check_registration_url='https://voterportal.sos.la.gov/', polling_location_url='https://voterportal.sos.la.gov/', absentee_ballot_url='https://www.sos.la.gov/ElectionsAndVoting/Vote/VoteByMail/Pages/default.aspx', local_election_url='https://voterportal.sos.la.gov/Registrar', ballot_tracker_url='https://voterportal.sos.la.gov/', absentee_application_in_person_deadline='Received by 4:30pm, 4 days before Election Day.', absentee_application_mail_deadline='Received by 4:30pm, 4 days before Election Day.', absentee_application_online_deadline='Received by 4:30pm, 4 days before Election Day.', voted_absentee_ballot_deadline='Received by 4:30pm, 1 day before Election Day (most voters). Election Day (hospitalized voters).')
ME = State(id='ME', name='Maine', capital='Augusta', registration_url='https://www.maine.gov/sos/cec/elec/voter-info/votreg.html',
           elections_url='https://www.maine.gov/sos/cec/elec/upcoming/index.html', registration_in_person_deadline='Election Day.', registration_mail_deadline='Received 15 business days before Election Day.', registration_online_deadline='N/A', check_registration_url='https://www.maine.gov/portal/government/edemocracy/voter_lookup.php', polling_location_url='http://www.maine.gov/portal/government/edemocracy/voter_lookup.php', absentee_ballot_url='https://www.maine.gov/sos/cec/elec/voter-info/absent.html', local_election_url='https://www.maine.gov/sos/cec/elec/munic.html', ballot_tracker_url='https://apps.web.maine.gov/cgi-bin/online/AbsenteeBallot/ballot_status.pl', absentee_application_in_person_deadline='Received 3 business days before Election Day.', absentee_application_mail_deadline='Received 3 business days before Election Day.', absentee_application_online_deadline='Received 3 business days before Election Day.', voted_absentee_ballot_deadline='Received Election Day.')
MD = State(id='MD', name='Maryland', capital='Annapolis', registration_url='https://elections.maryland.gov/voter_registration/index.html',
           elections_url='https://elections.maryland.gov/elections/', registration_in_person_deadline='21 days before Election Day. You may also register during early voting or on Election Day with proof of address. See Election Day registration instructions.', registration_mail_deadline='Postmarked 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://voterservices.elections.maryland.gov/votersearch', polling_location_url='https://voterservices.elections.maryland.gov/votersearch', absentee_ballot_url='https://elections.maryland.gov/voting/absentee.html', local_election_url='https://elections.maryland.gov/about/county_boards.html', ballot_tracker_url='https://voterservices.elections.maryland.gov/VoterSearch', absentee_application_in_person_deadline='Received 7 days before Election Day.', absentee_application_mail_deadline='Received 14 days before Election Day.', absentee_application_online_deadline='Received 14 days before Election Day.', voted_absentee_ballot_deadline='Postmarked on or before Election Day and received by 10am, 10 days after Election Day.')
MA = State(id='MA', name='Massachusetts', capital='Boston', registration_url='https://www.sec.state.ma.us/OVR/',
           elections_url='https://www.sec.state.ma.us/ele/elesched/schedidx.htm', registration_in_person_deadline='10 days before Election Day.', registration_mail_deadline='Postmarked 10 days before Election Day.', registration_online_deadline='10 days before Election Day.', check_registration_url='https://www.sec.state.ma.us/VoterRegistrationSearch/MyVoterRegStatus.aspx', polling_location_url='https://www.sec.state.ma.us/VoterRegistrationSearch/MyVoterRegStatus.aspx', absentee_ballot_url='https://www.sec.state.ma.us/ele/eleabsentee/absidx.htm', local_election_url='https://www.sec.state.ma.us/ele/eleev/ev-find-my-election-office.htm', ballot_tracker_url='https://www.sec.state.ma.us/wheredoivotema/track/trackmyballot.aspx', absentee_application_in_person_deadline='Received by noon, 1 day before Election Day, but we recommend applying at least 7 days before Election Day', absentee_application_mail_deadline='Received by noon, 1 day before Election Day, but we recommend applying at least 7 days before Election Day', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day.')
MI = State(id='MI', name='Michigan', capital='Lansing', registration_url='https://mvic.sos.state.mi.us/Home/RegisterToVote',
           elections_url='https://www.michigan.gov/sos/0,4670,7-127-1633---,00.html', registration_in_person_deadline='Any time up to 8:00 p.m. on Election Day at your city or township clerk office. The voter registration deadline is 15 days before Election Day, if you submit an application form through a voter registration drive or deliver it to a county clerk or secretary of state office.', registration_mail_deadline='Postmarked 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://mvic.sos.state.mi.us/', polling_location_url='https://webapps.sos.state.mi.us/M.MVIC/Pages/VoterSearch.aspx', absentee_ballot_url='https://mvic.sos.state.mi.us/Home/VoteAtHome', local_election_url='https://www.michigan.gov/sos/0,4670,7-127-1633_8716-21041--,00.html', ballot_tracker_url='https://mvic.sos.state.mi.us/Voter/Index', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 4 days before Election Day.', absentee_application_online_deadline='Received 4 days before Election Day.', voted_absentee_ballot_deadline='Received by the time the polls close on Election Day.')
MN = State(id='MN', name='Minnesota', capital='St. Paul', registration_url='https://www.sos.state.mn.us/elections-voting/register-to-vote/',
           elections_url='https://www.sos.state.mn.us/election-administration-campaigns/elections-calendar/', registration_in_person_deadline='Election Day.', registration_mail_deadline='Received 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://mnvotes.sos.state.mn.us/VoterStatus.aspx', polling_location_url='http://pollfinder.sos.state.mn.us/', absentee_ballot_url='https://www.sos.state.mn.us/elections-voting/other-ways-to-vote', local_election_url='https://www.sos.state.mn.us/elections-voting/find-county-election-office/', ballot_tracker_url='https://mnvotes.sos.state.mn.us/AbsenteeBallotStatus.aspx', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='Received 1 day before Election Day.', voted_absentee_ballot_deadline='Received by 8pm on Election Day if by mail or received by 3pm on Election Day if they are hand-delivered to a drop box or elections office.')
MS = State(id='MS', name='Mississippi', capital='Jackson', registration_url='https://www.sos.state.mn.us/elections-voting/register-to-vote/',
           elections_url='https://www.sos.ms.gov/elections-voting', registration_in_person_deadline='30 days before Election Day.', registration_mail_deadline='Postmarked 30 days before Election Day.', registration_online_deadline='N/A', check_registration_url='https://www.msegov.com/sos/voter_registration/AmIRegistered', polling_location_url='http://www.sos.ms.gov/pollingplace/pages/default.aspx', absentee_ballot_url='https://www.fvap.gov/uploads/FVAP/Forms/fwab2013.pdf', local_election_url='https://sos.ms.gov/elections-voting/county-election-information', absentee_application_in_person_deadline='No specific deadline. We recommend requesting your ballot at least 7 days before Election Day. In-person absentee voting for those with a qualifying excuse ends 3 days before Election Day.', absentee_application_mail_deadline='No specific deadline. We recommend requesting your ballot at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received within 5 business days of Election Day (by mail); Received 3 days before Election Day (in person).')
MO = State(id='MO', name='Missouri', capital='Jefferson City', registration_url='https://www.sos.mo.gov/elections/goVoteMissouri/register',
           elections_url='https://www.sos.mo.gov/elections/calendar/', registration_in_person_deadline='27 days before Election Day.', registration_mail_deadline='Postmarked 27 days before Election Day.', registration_online_deadline='27 days before Election Day.', check_registration_url='https://s1.sos.mo.gov/elections/voterlookup/', polling_location_url='https://voteroutreach.sos.mo.gov/PRD/VoterOutreach/VOSearch.aspx', absentee_ballot_url='https://www.sos.mo.gov/elections/goVoteMissouri/howtovote#absentee', local_election_url='https://www.sos.mo.gov/elections/govotemissouri/localelectionauthority', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 13 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day by closing of the polls (7pm).')
MT = State(id='MT', name='Montana', capital='Helena', registration_url='https://sosmt.gov/elections/vote/',
           elections_url='https://sosmt.gov/elections/calendars/', registration_in_person_deadline='Election Day.', registration_mail_deadline='Postmarked 8 days before Election Day and received 5 days before Election Day.', registration_online_deadline='N/A', check_registration_url='https://app.mt.gov/voterinfo/', polling_location_url='https://app.mt.gov/voterinfo/', absentee_ballot_url='https://sosmt.gov/elections/vote/#how-to-vote-by-absentee-ballot', local_election_url='https://sosmt.gov/elections/', ballot_tracker_url='https://app.mt.gov/voterinfo/', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received by noon, 1 day before before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 8pm on Election Day.')
NE = State(id='NE', name='Nebraska', capital='Lincoln', registration_url='https://www.nebraska.gov/apps-sos-voter-registration/',
           elections_url='https://www.nebraska.gov/featured/elections-voting/', registration_in_person_deadline='11 days before Election Day.', registration_mail_deadline='Postmarked 18 days before Election Day. Received 14 days before Election Day, if there\'s an illegible postmark.', registration_online_deadline='18 days before Election Day', check_registration_url='https://www.votercheck.necvr.ne.gov/VoterView/RegistrantSearch.do', polling_location_url='https://www.votercheck.necvr.ne.gov/VoterView/PollingPlaceSearch.do', absentee_ballot_url='https://sos.nebraska.gov/elections/general-voter-information#early', local_election_url='https://sos.nebraska.gov/elections/election-officials-contact-information', ballot_tracker_url='https://www.votercheck.necvr.ne.gov/VoterView/AbsenteeBallotSearch.do', absentee_application_in_person_deadline='Received 11 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day.')
NV = State(id='NV', name='Nevada', capital='Carson City', registration_url='https://www.nvsos.gov/sos/elections/voters/registering-to-vote',
           elections_url='https://www.nvsos.gov/sos/elections/election-information', registration_in_person_deadline='Election Day.', registration_mail_deadline='Postmarked 28 days before Election Day.', registration_online_deadline='5 days before Election Day.', check_registration_url='https://nvsos.gov/votersearch/', polling_location_url='https://www.nvsos.gov/votersearch/', absentee_ballot_url='https://www.nvsos.gov/sos/elections/voters/absentee-voting', local_election_url='https://www.nvsos.gov/sos/elections/voters/county-clerk-contact-information', ballot_tracker_url='https://nevada.ballottrax.net/voter/', absentee_application_in_person_deadline='Received 14 days before Election Day.', absentee_application_mail_deadline='Received 14 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked on or before Election Day.')
NH = State(id='NH', name='New Hampshire', capital='Concord', registration_url='https://sos.nh.gov/elections/voters/register-to-vote/',
           elections_url='https://www.ncsbe.gov/voting/upcoming-election', registration_in_person_deadline='Election Day. Before Election Day, the last day to register is the last meeting of the Supervisors of the Checklist. The supervisors meet once, 6-13 days before Election Day. Check your town/city website, or call your clerk\'s office for the date, time, and location of the Supervisor\'s meeting.', registration_mail_deadline='Received between 6 and 13 days before Election Day, depending on which town you live in.', registration_online_deadline='N/A', check_registration_url='https://app.sos.nh.gov/Public/PartyInfo.aspx', polling_location_url='http://app.sos.nh.gov/Public/PollingPlaceSearch.aspx', absentee_ballot_url='https://sos.nh.gov/elections/voters/register-to-vote/registering-to-vote-in-new-hampshire/', local_election_url='https://justfacts.votesmart.org/elections/offices/NH', ballot_tracker_url='https://app.sos.nh.gov/Public/AbsenteeBallot.aspx', absentee_application_in_person_deadline='No specific deadline.', absentee_application_mail_deadline='No specific deadline. We recommend requesting your ballot at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 5pm Election Day.')
NJ = State(id='NJ', name='New Jersey', capital='Trenton', registration_url='https://nj.gov/state/elections/voter-registration.shtmll',
           elections_url='https://www.state.nj.us/state/elections/election-information.shtml', registration_in_person_deadline='21 days before Election Day.', registration_mail_deadline='Postmarked 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://voter.svrs.nj.gov/registration-check', polling_location_url='https://voter.njsvrs.com/elections/polling-lookup.html', absentee_ballot_url='https://nj.gov/state/elections/vote-by-mail.shtml', local_election_url='https://www.state.nj.us/state/elections/vote-county-election-officials.shtml', ballot_tracker_url='https://www.nj.gov/state/elections/vote-track-my-ballot.shtml', absentee_application_in_person_deadline='Received by 3pm, the day before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received 144 hours after polls close.')
NM = State(id='NM', name='New Mexico', capital='Santa Fe', registration_url='https://portal.sos.state.nm.us/OVR/WebPages/InstructionsStep1.aspx',
           elections_url='https://www.sos.state.nm.us/voting-and-elections/upcoming-elections/', registration_in_person_deadline='Saturday before Election Day at the county clerk\'s office. 28 days before Election Day otherwise.', registration_mail_deadline='Postmarked 28 days before Election Day. However, an application may be accepted through the Friday following the deadline if the application is postmarked before the deadline.', registration_online_deadline='28 days before Election Day.', check_registration_url='https://voterportal.servis.sos.state.nm.us/WhereToVote.aspx', polling_location_url='http://www.sos.state.nm.us/Voter_Information/voter-information-portal.aspx', absentee_ballot_url='https://portal.sos.state.nm.us/OVR/WebPages/AbsenteeApplication.aspx', local_election_url='https://www.sos.state.nm.us/voting-and-elections/voter-information-portal/county-clerk-information/', ballot_tracker_url='https://voterportal.servis.sos.state.nm.us/wheretovote.aspx', absentee_application_in_person_deadline='Received 14 days before Election Day.', absentee_application_mail_deadline='Received 14 days before Election Day.', absentee_application_online_deadline='Received 14 days before Election Day.', voted_absentee_ballot_deadline='Received by 7pm Election Day.')
NY = State(id='NY', name='New York', capital='Albany', registration_url='https://www.elections.ny.gov/VotingRegister.html',
           elections_url='https://vote.nyc/page/upcoming-elections', registration_in_person_deadline='25 days before Election Day.', registration_mail_deadline='Postmarked 25 days before Election Day. Received 20 days before Election Day.', registration_online_deadline='25 days before Election Day.', check_registration_url='https://voterlookup.elections.ny.gov/', polling_location_url='https://voterlookup.elections.state.ny.us/votersearch.aspx', absentee_ballot_url='https://www.elections.ny.gov/VotingAbsentee.html', local_election_url='https://www.elections.ny.gov/countyboards.html', ballot_tracker_url='https://nycabsentee.com/tracking', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Postmarked 7 days before Election Day.', absentee_application_online_deadline='Received 7 days before Election Day.', voted_absentee_ballot_deadline='Postmarked on Election Day and received 7 days after Election Day. Voted ballots can also be turned in by hand on election day.')
NC = State(id='NC', name='North Carolina', capital='Raleigh', registration_url='https://www.ncsbe.gov/registering',
           elections_url='https://www.ncsbe.gov/voting/upcoming-election', registration_in_person_deadline='The Saturday before Election Day if voting early in person. Otherwise 25 days before Election Day.', registration_mail_deadline='Postmarked 25 days before Election Day. If the postmark is missing or unclear, the application will still be processed if it is Received 20 days before Election Day.', registration_online_deadline='25 days before Election Day.', check_registration_url='https://vt.ncsbe.gov/RegLkup/', polling_location_url='https://vt.ncsbe.gov/pplkup/', absentee_ballot_url='https://www.ncsbe.gov/voting/vote-mail', local_election_url='https://vt.ncsbe.gov/BOEInfo/', ballot_tracker_url='https://vt.ncsbe.gov/RegLkup/', absentee_application_in_person_deadline='Received by 5pm 7 days before Election Day.', absentee_application_mail_deadline='Received by 5pm, 7 days before Election Day.', absentee_application_online_deadline='Received 7 days before Election Day.', voted_absentee_ballot_deadline='For the 2020 general election, if in person, received by Election Day; if by mail, postmarked by Election Day and received by 5pm no later than 9 days after Election Day.')
ND = State(id='ND', name='North Dakota', capital='Bismarck', registration_url='https://vote.nd.gov/PortalListDetails.aspx?ptlhPKID=73&ptlPKID=5',
           elections_url='https://vip.sos.nd.gov/pdfs/Portals/electioncalendar.pdf', registration_in_person_deadline='North Dakota does not have voter registration. You simply need to bring valid proof of ID and residency to the polls in order to vote.', registration_mail_deadline='North Dakota does not have voter registration. You simply need to bring valid proof of ID and residency to the polls in order to vote.', registration_online_deadline='N/A', check_registration_url='https://vip.sos.nd.gov/PortalListDetails.aspx?ptlhPKID=79&ptlPKID=7', polling_location_url='https://vip.sos.nd.gov/wheretovote.aspx', absentee_ballot_url='https://vip.sos.nd.gov/absentee/Default.aspx', local_election_url='https://vip.sos.nd.gov/countyauditors.aspx', ballot_tracker_url='https://vip.sos.nd.gov/AbsenteeTracker.aspx', absentee_application_in_person_deadline='No specific deadline.', absentee_application_mail_deadline='No specific deadline. We recommend requesting your ballot at least 7 days before Election Day.', absentee_application_online_deadline='No specific deadline.', voted_absentee_ballot_deadline='Postmarked 1 day before Election Day.')
OH = State(id='OH', name='Ohio', capital='Columbus', registration_url='https://olvr.ohiosos.gov/',
           elections_url='https://www.ohiosos.gov/elections/voters/current-voting-schedule/', registration_in_person_deadline='30 days before Election Day, extended to the next business day if this falls on a Sunday.', registration_mail_deadline='Postmarked 30 days before Election Day, extended to the next business day if this falls on a Sunday.', registration_online_deadline='30 days before Election Day.', check_registration_url='https://voterlookup.ohiosos.gov/voterlookup.aspx', polling_location_url='https://voterlookup.ohiosos.gov/voterlookup.aspx', absentee_ballot_url='https://www.ohiosos.gov/elections/voters/how-to-request-your-absentee-ballot/', local_election_url='https://www.sos.state.oh.us/elections/elections-officials/county-boards-of-elections-directory/?__cf_chl_jschl_tk__=pmd_HdBrEuSYolyOjWo6MvTe4Dd0yOhDpWDBlUkoh45lNj0-1631120792-0-gqNtZGzNAiWjcnBszQil', ballot_tracker_url='https://www.sos.state.oh.us/elections/voters/toolkit/ballot-tracking/', absentee_application_in_person_deadline='Received by noon, 3 days before Election Day.', absentee_application_mail_deadline='Received by noon, 3 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked no later than the day before Election Day and received no later than 10 days after Election Day, or delivered in person on Election Day.')
OK = State(id='OK', name='Oklahoma', capital='Oklahoma City', registration_url='https://oklahoma.gov/elections/voter-info/register-to-vote.html',
           elections_url='https://hosting.okelections.us/electionlist.html', registration_in_person_deadline='25 days before Election Day.', registration_mail_deadline='Postmarked 25 days before Election Day.', registration_online_deadline='N/A', check_registration_url='https://okvoterportal.okelections.us/', polling_location_url='https://services.okelections.us/voterSearch.aspx', absentee_ballot_url='https://oklahoma.gov/elections/voter-info/absentee-voting.html', local_election_url='https://oklahoma.gov/elections/about-us/county-election-boards.html', ballot_tracker_url='https://okvoterportal.okelections.us/', absentee_application_in_person_deadline='Received 7 days before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='Received 7 days before Election Day.', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
OR = State(id='OR', name='Oregon', capital='Salem', registration_url='https://sos.oregon.gov/voting/Pages/registration.aspx?lang=en',
           elections_url='https://sos.oregon.gov/voting/Pages/current-election.aspx', registration_in_person_deadline='21 days before Election Day.', registration_mail_deadline='Received 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://secure.sos.state.or.us/orestar/vr/showVoterSearch.do?source=SOS', polling_location_url='http://sos.oregon.gov/voting/Pages/voteinor.aspx', absentee_ballot_url='https://sos.oregon.gov/voting/Pages/voteinor.aspx', local_election_url='https://sos.oregon.gov/elections/pages/countyofficials.aspx', ballot_tracker_url='https://secure.sos.state.or.us/orestar/vr/showVoterSearch.do?lang=eng', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 5 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 8pm on Election Day.')
PA = State(id='PA', name='Pennsylvania', capital='Harrisburg', registration_url='https://www.pavoterservices.pa.gov/Pages/VoterRegistrationApplication.aspx',
           elections_url='https://www.votespa.com/About-Elections/Pages/Upcoming-Elections.aspx', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Received 15 days before Election Day.', registration_online_deadline='15 days before Election Day.', check_registration_url='https://www.pavoterservices.pa.gov/Pages/VoterRegistrationStatus.aspx', polling_location_url='https://www.pavoterservices.state.pa.us/pages/pollingplaceinfo.aspx', absentee_ballot_url='https://www.votespa.com/Voting-in-PA/Pages/Mail-and-Absentee-Ballot.aspx', local_election_url='https://www.vote.pa.gov/Resources/Pages/Contact-Your-Election-Officials.aspx', ballot_tracker_url='https://www.vote.org/state/pennsylvania', absentee_application_in_person_deadline='Received 7 days before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='Received 7 days before Election Day.', voted_absentee_ballot_deadline='If delivered in-person, received by 8pm on Election Day. If mailed, postmarked by Election Day and received within 3 days after Election Day')
RI = State(id='RI', name='Rhode Island', capital='Providence', registration_url='https://vote.sos.ri.gov/Home/RegistertoVote?ActiveFlag=1',
           elections_url='https://elections.ri.gov/elections/upcoming/index.php', registration_in_person_deadline='30 days before Election Day.', registration_mail_deadline='Postmarked 30 days before Election Day. If the postmark is missing or unclear and the registration form is received no later than 5 days after the deadline, the individual shall be presumed to have been registered by the deadline.', registration_online_deadline='30 days before Election Day.', check_registration_url='https://vote.sos.ri.gov/Home/UpdateVoterRecord?ActiveFlag=0', polling_location_url='https://sos.ri.gov/vic/', absentee_ballot_url='https://vote.sos.ri.gov/Voter/VotebyMail', local_election_url='https://vote.sos.ri.gov/Elections/LocalBoards', ballot_tracker_url='https://vote.sos.ri.gov/Home/UpdateVoterRecord?ActiveFlag=3', absentee_application_in_person_deadline='Received by 4pm, 21 days before Election Day.', absentee_application_mail_deadline='Received by 4pm, 21 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 8pm on Election Day.')
SC = State(id='SC', name='South Carolina', capital='Columbia', registration_url='https://www.scvotes.gov/south-carolina-voter-registration-information',
           elections_url='https://www.scvotes.gov/schedule-elections', registration_in_person_deadline='30 days before Election Day. If this falls on a Sunday, the last preceding day that the county board of voter registration and elections is open.', registration_mail_deadline='Postmarked 30 days before Election Day, the deadline is extended to the next business day if this falls on a Sunday.', registration_online_deadline='30 days before Election Day.', check_registration_url='https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx?PagMode=VoterInfo', polling_location_url='https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx?PageMode=VoterInfo', absentee_ballot_url='https://www.scvotes.gov/absentee-voting', local_election_url='https://www.scvotes.gov/how-register-absentee-voting', ballot_tracker_url='https://info.scvotes.sc.gov/eng/voterinquiry/VoterInformationRequest.aspx?PageMode=AbsenteeInfo', absentee_application_in_person_deadline='4 days before Election Day, unless the individual is already a registered voter; then 1 day before Election Day', absentee_application_mail_deadline='Received 10 days before Election Day', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')
SD = State(id='SD', name='South Dakota', capital='Pierre', registration_url='https://sdsos.gov/elections-voting/voting/register-to-vote/default.aspx',
           elections_url='https://sdsos.gov/elections-voting/upcoming-elections/general-information/default.aspx', registration_in_person_deadline='15 days before Election Day.', registration_mail_deadline='Received 15 days before Election Day.', registration_online_deadline='N/A', check_registration_url='https://vip.sdsos.gov/viplogin.aspx', polling_location_url='https://vip.sdsos.gov/viplogin.aspx', absentee_ballot_url='https://sdsos.gov/elections-voting/voting/absentee-voting.aspx', local_election_url='https://vip.sdsos.gov/CountyAuditors.aspx', ballot_tracker_url='https://vip.sdsos.gov/VIPLogin.aspx', absentee_application_in_person_deadline='1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_mail_deadline='Received 1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day.')
TN = State(id='TN', name='Tennessee', capital='Nashville', registration_url='https://sos.tn.gov/products/elections/register-vote',
           elections_url='https://sos.tn.gov/elections/election-information', registration_in_person_deadline='30 days before Election Day. If this falls on a Sunday, 29 days before Election Day.', registration_mail_deadline='Postmarked 30 days before Election Day, the deadline is extended to the next business day if this falls on a Sunday.', registration_online_deadline='30 days before Election Day.', check_registration_url='https://tnmap.tn.gov/voterlookup/', polling_location_url='https://web.go-vote-tn.elections.tn.gov/', absentee_ballot_url='https://sos.tn.gov/products/elections/absentee-voting', local_election_url='https://sos.tn.gov/products/elections/find-your-county-election-commission', ballot_tracker_url='https://tnmap.tn.gov/voterlookup/', absentee_application_in_person_deadline='Received 7 days before Election Day.', absentee_application_mail_deadline='Received 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received Election Day.')
TX = State(id='TX', name='Texas', capital='Austin', registration_url='https://www.votetexas.gov/register/index.html',
           elections_url='https://www.sos.state.tx.us/elections/voter/important-election-dates.shtml', registration_in_person_deadline='30 days before Election Day. If this falls on a Sunday, 29 days before Election Day.', registration_mail_deadline='Postmarked 30 days before Election Day, the deadline is extended to the next business day if this falls on a Sunday.', registration_online_deadline='N/A', check_registration_url='https://teamrv-mvp.sos.texas.gov/MVP/mvp.do', polling_location_url='https://teamrv-mvp.sos.texas.gov/MVP/mvp.do', absentee_ballot_url='https://www.sos.texas.gov/elections/voter/reqabbm.shtml', local_election_url='https://www.sos.state.tx.us/elections/voter/cclerks.shtml', absentee_application_in_person_deadline='Received 22 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='Received 11 days before Election Day.', voted_absentee_ballot_deadline='Postmarked by Election Day and received by the day after Election Day.')
UT = State(id='UT', name='Utah', capital='Salt Lake City', registration_url='https://voteinfo.utah.gov/learn-about-registering-to-vote/',
           elections_url='https://voteinfo.utah.gov/election-dates-deadlines/', registration_in_person_deadline='7 days before Election Day in clerk\'s office, but may also register during early vote and on Election Day. However, individuals must vote by provisional ballot if they register in person during early voting or on Election Day.', registration_mail_deadline='Received 11 days before Election Day, the deadline is extended to the next business day if this falls on a Sunday.', registration_online_deadline='11 days before Election Day.', check_registration_url='https://votesearch.utah.gov/voter-search/search/search-by-voter/voter-info', polling_location_url='https://votesearch.utah.gov/voter-search/search/search-by-address/how-and-where-can-i-vote', absentee_ballot_url='https://voteinfo.utah.gov/learn-about-voting-by-mail-and-absentee-voting/', local_election_url='https://elections.utah.gov/election-resources/county-clerks', ballot_tracker_url='https://votesearch.utah.gov/voter-search/search/search-by-voter/track-mail-ballot', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='If you need to change where your ballot is mailed, submit address change at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='If in-person, received by Election Day; if mailed, postmarked 1 day before Election Day and received before noon on the day of the county canvass.')
VT = State(id='VT', name='Vermont', capital='Montpelier', registration_url='https://sos.vermont.gov/elections/voters/registration/',
           elections_url='https://sos.vermont.gov/elections-calendar/', registration_in_person_deadline='Election Day (you must show proof of residence to register at the polls on Election Day).', registration_mail_deadline='Received Election Day.', registration_online_deadline='Election Day. But if you register online the day before or on Election Day, your application may not be processed and your name may not appear on the checklist and you may be asked to fill out another application at the polls. To be sure your name appears on the checklist, please register by the Friday before the election.', check_registration_url='https://mvp.sec.state.vt.us/', polling_location_url='https://www.sec.state.vt.us/elections/voters.aspx', absentee_ballot_url='https://sos.vermont.gov/elections/voters/early-absentee-voting/', local_election_url='https://sos.vermont.gov/elections/town-clerks/', ballot_tracker_url='https://mvp.vermont.gov/', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='Received 1 day before Election Day.', voted_absentee_ballot_deadline='Received Election Day.')
VA = State(id='VA', name='Virginia', capital='Richmond', registration_url='https://www.elections.virginia.gov/registration/',
           elections_url='https://www.elections.virginia.gov/casting-a-ballot/calendars-schedules/upcoming-elections.html', registration_in_person_deadline='Received by close of business 22 days before Election Day.', registration_mail_deadline='Postmarked 22 days before Election Day.', registration_online_deadline='Received by 11:59 PM 22 days before Election Day.', check_registration_url='https://vote.elections.virginia.gov/VoterInformation', polling_location_url='https://vote.elections.virginia.gov/VoterInformation/PollingPlaceLookup', absentee_ballot_url='https://www.elections.virginia.gov/casting-a-ballot/absentee-voting/', local_election_url='https://vote.elections.virginia.gov/voterinformation/publiccontactlookup', ballot_tracker_url='https://www.elections.virginia.gov/citizen-portal/', absentee_application_in_person_deadline='Received 3 days before Election Day.', absentee_application_mail_deadline='Received 11 days before Election Day.', absentee_application_online_deadline='Received 11 days before Election Day.', voted_absentee_ballot_deadline='Postmarked by Election Day and received by noon 3 days after Election Day.')
WA = State(id='WA', name='Washington', capital='Olympia', registration_url='https://voter.votewa.gov/WhereToVote.aspx',
           elections_url='https://www.elections.virginia.gov/casting-a-ballot/calendars-schedules/upcoming-elections.html', registration_in_person_deadline='Election Day.', registration_mail_deadline='Received 8 days before Election Day.', registration_online_deadline='8 days before Election Day.', check_registration_url='https://www.sos.wa.gov/elections/myvote/', polling_location_url='https://www.sos.wa.gov/elections/', absentee_ballot_url='https://www.sos.wa.gov/elections/faq_vote_by_mail.aspx', local_election_url='https://www.sos.wa.gov/elections/auditors/', ballot_tracker_url='https://voter.votewa.gov/WhereToVote.aspx#/login', absentee_application_in_person_deadline='N/A', absentee_application_mail_deadline='No specific deadline. We recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Postmarked by Election Day and received 5 days after Election Day.')
WV = State(id='WV', name='West Virginia', capital='Charleston', registration_url='https://ovr.sos.wv.gov/Register/Landing',
           elections_url='https://sos.wv.gov/elections/Pages/default.aspx', registration_in_person_deadline='21 days before Election Day.', registration_mail_deadline='Postmarked 21 days before Election Day.', registration_online_deadline='21 days before Election Day.', check_registration_url='https://apps.sos.wv.gov/elections/voter/', polling_location_url='https://services.sos.wv.gov/Elections/Voter/FindMyPollingPlace', absentee_ballot_url='https://sos.wv.gov/elections/Pages/AbsenteeVotingInformation.aspx', local_election_url='https://sos.wv.gov/elections/Pages/CountyClerkDirectory.aspx', ballot_tracker_url='https://services.sos.wv.gov/Elections/Voter/AbsenteeBallotTracking', absentee_application_in_person_deadline='Received 6 days before Election Day.', absentee_application_mail_deadline='Received 6 days before Election Day.', absentee_application_online_deadline='Received 6 days before Election Day.', voted_absentee_ballot_deadline='Postmarked by Election Day and received by 6 days after Election Day. (Ballots with no postmark will be counted if received by 1 day after Election Day.)')
WI = State(id='WI', name='Wisconsin', capital='Madison', registration_url='https://myvote.wi.gov/en-us/Register-To-Vote',
           elections_url='https://elections.wi.gov/elections-voting/elections', registration_in_person_deadline='The Friday before Election Day.', registration_mail_deadline='Postmarked 20 days before Election Day.', registration_online_deadline='20 days before Election Day.', check_registration_url='https://myvote.wi.gov/en-us/Register-To-Vote', polling_location_url='https://myvote.wi.gov/en-US/FindMyPollingPlace', absentee_ballot_url='https://myvote.wi.gov/en-us/Vote-Absentee', local_election_url='https://elections.wi.gov/clerks/directory', ballot_tracker_url='https://myvote.wi.gov/en-us/My-Voter-Info', absentee_application_in_person_deadline='Received 5 days before Election Day.', absentee_application_mail_deadline='Received 5 days before Election Day.', absentee_application_online_deadline='Received 5 days before Election Day.', voted_absentee_ballot_deadline='Received by 8pm on Election Day.')
WY = State(id='WY', name='Wyoming', capital='Cheyenne', registration_url='https://sos.wyo.gov/Elections/State/RegisteringToVote.aspx',
           elections_url='https://sos.wyo.gov/Elections/Default.aspx', registration_in_person_deadline='14 days before Election Day.', registration_mail_deadline='Postmarked 14 days before Election Day. After this date, individuals may register to vote by mail if their registration is also accompanied by an absentee ballot request.', registration_online_deadline='N/A', check_registration_url='https://sos.wyo.gov/Elections/Docs/WYCountyClerks.pdf', polling_location_url='http://soswy.state.wy.us/Elections/PollPlace/Default.aspx', absentee_ballot_url='https://sos.wyo.gov/Elections/State/AbsenteeVoting.aspx', local_election_url='https://sos.wyo.gov/Elections/Docs/WYCountyClerks.pdf', absentee_application_in_person_deadline='Received 1 day before Election Day.', absentee_application_mail_deadline='Received 1 day before Election Day, but we recommend applying at least 7 days before Election Day.', absentee_application_online_deadline='N/A', voted_absentee_ballot_deadline='Received by 7pm on Election Day.')

db.session.add_all([AK, AL, AR, AZ, CA, CO, CT, DE, DC, FL, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI,
                   MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY])
db.session.commit()


r1 = RegistrationRule(rule='You must be a citizen of the United States')
r2 = RegistrationRule(
    rule='You must be a resident of Alabama and your county at the time of registration')
r3 = RegistrationRule(rule='You must be 18 years old before any election')
r4 = RegistrationRule(
    rule='You must not have been convicted of a disqualifying felony')
r5 = RegistrationRule(
    rule='You must not currently be declared mentally incompetent through a competency hearing')
r6 = RegistrationRule(rule='You must swear or affirm to "support and defend the Constitution of the US and the State of Alabama and further disavow any belief or affiliation with any group which advocates the overthrow of the governments of the US or the State of Alabama by unlawful means and that the information contained herein is true, so help me God."')
r7 = RegistrationRule(
    rule='You must be at least 18 years old within 90 days of completing your registration')
r8 = RegistrationRule(rule='You must be a resident of Alaska')
r9 = RegistrationRule(
    rule='You must not be a convicted felon (unless unconditionally discharged)')
r10 = RegistrationRule(
    rule='You must not be registered to vote in another state')
r11 = RegistrationRule(
    rule='You must be a resident of Arizona and your county at least 29 days preceeding the next election')
r12 = RegistrationRule(
    rule='You must be 18 years old on or before the next general election')
r13 = RegistrationRule(
    rule='You must be able to write your name or mark, unless prevented from so doing by physical disability')
r14 = RegistrationRule(
    rule='You must not have been convicted of treason or a felony (or have had your civil rights restored)')
r15 = RegistrationRule(
    rule='You must not currently be declared an incapacitated person by a court of law')
r16 = RegistrationRule(
    rule='You must live in Arkansas at the address in Box 2 on the application')
r17 = RegistrationRule(
    rule='You must be at least 18 years old before the next election')
r18 = RegistrationRule(
    rule='You must not be a convicted felon (or have completely discharged your sentence or been pardoned)')
r19 = RegistrationRule(
    rule='You must not claim the right to vote in any other jurisdiction')
r20 = RegistrationRule(
    rule='You must not previously be adjudged mentally incompetent by a court of competent jurisdiction')
r21 = RegistrationRule(rule='You must be a resident of California')
r22 = RegistrationRule(
    rule='You must be at least 18 years of age at the time of the next election')
r23 = RegistrationRule(
    rule='You must not currently be serving a state or federal prison term for the conviction of a felony')
r24 = RegistrationRule(
    rule='You must not currently be judged mentally incompetent by a court of law.')
r25 = RegistrationRule(
    rule='You must be a resident of Colorado 22 days prior to Election Day')
r26 = RegistrationRule(
    rule='You must be 18 years old on or before Election Day')
r27 = RegistrationRule(
    rule='You must not be serving a sentence of detention, confinement, or parole for a felony conviction')
r28 = RegistrationRule(
    rule='You must be a resident of Connecticut and of the town in which you wish to vote')
r29 = RegistrationRule(
    rule='You must be at least 18 years old on the next election')
r30 = RegistrationRule(
    rule='You must have completed confinement and parole if previously convicted of a felony')
r31 = RegistrationRule(rule='You must be be a permanent resident of Delaware')
r32 = RegistrationRule(
    rule='You must be at least 18 years old on the date of the next general election')
r33 = RegistrationRule(rule='You must not be mentally incompetent')
r34 = RegistrationRule(rule='If you are a felon, you are eligible to vote as long as you have served your sentence (including parole) and your convictions were not for disqualifying felonies: murder and manslaughter (except vehicular homicide), sexual offenses, or crimes against public administration involving bribery or improper influence or abuse of office')
r35 = RegistrationRule(
    rule='You must be a District of Columbia resident at least 30 days preceding the next election')
r36 = RegistrationRule(
    rule='You must be at least 18 years old on or preceding the next general election')
r37 = RegistrationRule(
    rule='You must not be in prison for a felony conviction')
r38 = RegistrationRule(
    rule='You must not have been judged legally incompetent by a court of law')
r39 = RegistrationRule(
    rule='You must not claim the right to vote anywhere outside DC')
r40 = RegistrationRule(
    rule='You must be a legal resident of both the State of Florida and of the county in which you seek to be registered')
r41 = RegistrationRule(
    rule='You must be 18 years old (you may pre‑register if you are at least 16)')
r42 = RegistrationRule(
    rule='You must not be adjudicated mentally incapacitated with respect to voting in Florida or any other State, or if you have, you must first have your voting rights restored')
r43 = RegistrationRule(
    rule='You must not be a convicted felon, or if you are, you must first have your civil rights restored if they were taken away')
r44 = RegistrationRule(rule='You must swear or affirm the following: “I do solemnly swear (or affirm) that I will protect and defend the Constitution of the United States and the Constitution of the State of Florida, that I am qualified to register as an elector under the Constitution and laws of the State of Florida, and that all information provided in this application is true.”')
r45 = RegistrationRule(
    rule='You must be a legal resident of Georgia and of the county in which you want to vote')
r46 = RegistrationRule(
    rule='You must be at least 18 years old within six months after the day of registration, and be 18 years old to vote')
r47 = RegistrationRule(
    rule='You must not be serving a sentence for having been convicted of a felony involving moral turpitud')
r48 = RegistrationRule(
    rule='You must not have been judicially determined to be mentally incompetent, unless the disability has been removed')
r49 = RegistrationRule(rule='You must be a resident of the State of Hawaii')
r50 = RegistrationRule(
    rule='You must be at least 16 years old (you must be 18 years old by Election Day in order to vote)')
r51 = RegistrationRule(
    rule='You must not be incarcerated for a felony conviction')
r52 = RegistrationRule(
    rule='You must not be adjudicated by a court as “non compos mentis”')
r53 = RegistrationRule(rule='You must be at least 18 years old')
r54 = RegistrationRule(
    rule='You must have resided in Idaho and in the county for 30 days prior to the day of election')
r55 = RegistrationRule(
    rule='You must not be serving a sentence of imprisonment for a felony.  Your voting rights are restored once you have completed your sentence, probation, and parole')
r56 = RegistrationRule(
    rule='You must be a resident of Illinois and of your election precinct at least 30 days before the next election')
r57 = RegistrationRule(
    rule='You must be at least 18 years old on or before the next election')
r58 = RegistrationRule(
    rule='You must not be in jail for a felony conviction (but you can vote if you have completed your sentence)')
r59 = RegistrationRule(
    rule='You must not claim the right to vote anywhere else')
r60 = RegistrationRule(
    rule='You must have resided in the precinct at least 30 days before the next election')
r61 = RegistrationRule(
    rule='You must be at least 18 years of age on the day of the next general election')
r62 = RegistrationRule(
    rule='You must not currently be incarcerated for a criminal conviction')
r63 = RegistrationRule(rule='You must be a resident of Iowa')
r64 = RegistrationRule(
    rule='You must be at least 17 years old (you must be 18 to vote)')
r65 = RegistrationRule(
    rule='You must not have been convicted of a felony (or have had your rights restored)')
r66 = RegistrationRule(
    rule='You must not currently be judged by a court to be "incompetent to vote"')
r67 = RegistrationRule(
    rule='You must not claim the right to vote in more than one place')
r68 = RegistrationRule(rule='You must be a resident of Kansas')
r69 = RegistrationRule(rule='You must be 18 by the next election')
r70 = RegistrationRule(
    rule='You must have completed the terms of your sentence if convicted of a felony and recieved a certificate of discharge; a person serving a sentence for a felony conviction is ineligible to vote')
r71 = RegistrationRule(
    rule='You must not claim the right to vote in any other location or under any other name')
r72 = RegistrationRule(
    rule='You must be a resident of Kentucky for at least 28 days before to Election Day')
r73 = RegistrationRule(
    rule='You must be 18 years of age on or before the next general election')
r74 = RegistrationRule(
    rule='You must not be a convicted felon or if you have been convicted of a felony, your civil rights must have been restored by executive pardon')
r75 = RegistrationRule(
    rule='You must not have been judged “mentally incompetent” in a court of law')
r76 = RegistrationRule(
    rule='You must not claim the right to vote anywhere outside Kentucky')
r77 = RegistrationRule(rule='You must be a resident of Louisiana (Residence address must be address where you claim homestead exemption, if any, except for a resident in a nursing home or veteran’s home who may select to use the address of the nursing home or veterans’ home or the home where he has a homestead exemption. A college student may elect to use his home address or his address while away at school.)')
r78 = RegistrationRule(rule='You must be at least 17 years old (16 years old if registering in person at the Registrar of Voters Office or at the Louisiana Office of Motor Vehicles), and be 18 years old prior to the next election to vote')
r79 = RegistrationRule(rule='You must not currently be under an order of imprisonment for conviction of a felony. (If you are under an order but have not been incarcerated within the last five years, you ARE eligible to vote unless your conviction was for election fraud.)')
r80 = RegistrationRule(
    rule='You must not currently be under a judgment of interdiction for mental incompetence')
r81 = RegistrationRule(
    rule='You must be a resident of Maine and the municipality in which you want to vote')
r82 = RegistrationRule(
    rule='You must be 17 years old (you must be at least 18 years of age to vote, except that in primary elections you may vote if you are 17 but will be 18 by the general election)')
r83 = RegistrationRule(rule='You must be a Maryland resident')
r84 = RegistrationRule(
    rule='You must be at least 18 years old by the next general election')
r85 = RegistrationRule(
    rule='You must not be under guardianship for mental disability')
r86 = RegistrationRule(
    rule='You must not have been convicted of buying or selling votes')
r87 = RegistrationRule(
    rule='You must not have been convicted of a felony, or if you have, have completed serving a court ordered sentence of imprisonment')
r88 = RegistrationRule(rule='You must be a resident of Massachusetts')
r89 = RegistrationRule(
    rule='You must be 18 years old on or before the next election')
r90 = RegistrationRule(
    rule='You must not have been convicted of corrupt practices in respect to elections')
r91 = RegistrationRule(
    rule='You must not be under guardianship with respect to voting')
r92 = RegistrationRule(
    rule='You must not be currently incarcerated for a felony conviction')
r93 = RegistrationRule(rule='You must be 18 years old by the next election')
r94 = RegistrationRule(
    rule='You must be a resident of Michigan and at least a 30 day resident of your city or township by Election Day')
r95 = RegistrationRule(
    rule='You must not be confined in a jail after being convicted and sentenced')
r96 = RegistrationRule(
    rule='You must be a resident of Minnesota for 20 days before the next election')
r97 = RegistrationRule(
    rule='You must maintain residence at the address given on the registration form')
r98 = RegistrationRule(
    rule='You must be at least 18 years old on Election Day')
r99 = RegistrationRule(
    rule='You must if previously convicted of a felony, have completed or been discharged from your sentence')
r100 = RegistrationRule(
    rule='You must not be under a court‑ordered guardianship in which the right to vote has been revoked')
r101 = RegistrationRule(
    rule='You must not be found by a court to be legally incompetent to vote')
r102 = RegistrationRule(
    rule='You must have lived in Mississippi and in your county (and city, if applicable) 30 days before Election Day')
r103 = RegistrationRule(
    rule='You must be 18 years old by the time of the general election in which you want to vote')
r104 = RegistrationRule(rule='You must have not been convicted of voter fraud, murder, rape, bribery, theft, arson, obtaining money or goods under false pretense, perjury, forgery, embezzlement, bigamy, armed robbery, extortion, felony bad check, felony shoplifting, larceny, receiving stolen property, robbery, timber larceny, unlawful taking of a motor vehicle, statutory rape, carjacking, or larceny under lease or rental agreement, or have had your rights restored as required by law')
r105 = RegistrationRule(
    rule='You must not have been declared mentally incompetent by a court')
r106 = RegistrationRule(rule='You must be a resident of Missouri')
r107 = RegistrationRule(
    rule='You must be at least 17‑1/2 years of age (you must be 18 to vote)')
r108 = RegistrationRule(
    rule='You must not be on probation or parole after conviction of a felony, until finally discharged from such probation or parole')
r109 = RegistrationRule(
    rule='You must not be convicted of a felony or misdemeanor connected with the right of suffrage')
r110 = RegistrationRule(
    rule='You must not be adjudged incapacitated by any court of law')
r111 = RegistrationRule(
    rule='You must not be confined under a sentence of imprisonment')
r112 = RegistrationRule(
    rule='You must be at least 18 years old on or before Election Day')
r113 = RegistrationRule(
    rule='You must be a resident of Montana and of the county in which you want to vote for at least 30 days before the next election')
r114 = RegistrationRule(
    rule='You must not be in a penal institution for a felony conviction')
r115 = RegistrationRule(
    rule='You must not currently be determined by a court to be of unsound mind')
r116 = RegistrationRule(
    rule='You must meet these qualifications by the next Election Day if you do not currently meet them')
r117 = RegistrationRule(rule='You must be a resident of Nebraska')
r118 = RegistrationRule(
    rule='You must be at least 18 years of age or will be 18 years of age on or before the first Tuesday after the first Monday of November')
r119 = RegistrationRule(
    rule='You must not have been convicted of a felony, or if convicted, two years have passed since the sentence was completed (including any parole)')
r120 = RegistrationRule(
    rule='You must not have been officially found to be mentally incompetent')
r121 = RegistrationRule(
    rule='You must not have been convicted of treason, unless you have had your civil rights stored.')
r122 = RegistrationRule(
    rule='You must have attained the age of 18 years on the date of the next election')
r123 = RegistrationRule(
    rule='You must have continuously resided in the State of Nevada, in your county, at least 30 days and in your precinct at least 10 days before the next election')
r124 = RegistrationRule(
    rule='You must not currently be serving a term of imprisonment for a felony conviction')
r125 = RegistrationRule(
    rule='You must not be determined by a court of law to be mentally incompetent')
r126 = RegistrationRule(
    rule='You must claim no other place as your legal residence')
r127 = RegistrationRule(
    rule='You must be 18 years of age or older on Election Day')
r128 = RegistrationRule(
    rule='You must register to vote only in the town or ward in which you actually live')
r129 = RegistrationRule(
    rule='You must not have been convicted of a felony, unless you are past your final discharge')
r130 = RegistrationRule(
    rule='You must not have been ever convicted of bribery or intimidation relating to elections')
r131 = RegistrationRule(
    rule='You must be at least 17 years of age; you may register to vote if you are at least 17 years old but cannot vote until reaching the age of 18')
r132 = RegistrationRule(
    rule='You must be a resident of New Jersey and your county and at your address at least 30 days before the next election')
r133 = RegistrationRule(
    rule='You must not be serving a sentence of incarceration as the result of a conviction of any indictable offense under the laws of New Jersey or another state or of the United States')
r134 = RegistrationRule(
    rule='You must not be declared mentally incompetent by a court')
r135 = RegistrationRule(
    rule='You must be a resident of the State of New Mexico')
r136 = RegistrationRule(
    rule='You must be 18 years of age at the time of the next election')
r137 = RegistrationRule(
    rule='You must not have been denied the right to vote by a court of law by reason of mental incapacity')
r138 = RegistrationRule(rule='You must not be currently incarcerated or serving parole or supervised probation for a felony conviction (or if you have been convicted of a felony, have completed all the terms and conditions of sentencing, have been granted a pardon by the Governor, or have had your conviction overturned on appeal)')
r139 = RegistrationRule(
    rule='You must be a resident of New York and the county, city, or village for at least 30 days before Election Day')
r140 = RegistrationRule(
    rule='16- and 17-year-olds may preregister to vote, but cannot vote until they are 18')
r141 = RegistrationRule(
    rule='You must not be in prison or on parole for a felony conviction (unless parolee pardoned or restored rights of citizenship)')
r142 = RegistrationRule(
    rule='You must not currently be judged incompetent by a court')
r143 = RegistrationRule(rule='You must not claim the right to vote elsewhere')
r144 = RegistrationRule(
    rule='You must be a resident of North Carolina and the precinct in which you live for at least 30 days prior to Election Day')
r145 = RegistrationRule(
    rule='16- and 17-year-olds may preregister to vote, but cannot vote until they are 18 (17-year-olds may vote in a primary election if they will be 18 at the time of the general election)')
r146 = RegistrationRule(
    rule='You must not be currently serving a felony sentence, including probation, parole, or post-release supervision')
r147 = RegistrationRule(rule='You must be a resident of North Dakota')
r148 = RegistrationRule(
    rule='You must reside in the precinct for 30 days preceding Election Day')
r149 = RegistrationRule(
    rule='You must be able to provide a drivers license, non-driver identification card or other approved form of identification')
r150 = RegistrationRule(
    rule='You must be at least 18 years old on or before the next general election')
r151 = RegistrationRule(
    rule='You must be a resident of Ohio for at least 30 days immediately before the election in which you want to vote')
r152 = RegistrationRule(
    rule='You must not be currently incarcerated (in jail or prison) for a felony conviction. If you are an ex-felon and not currently incarcerated, you are eligible to vote in Ohio but you MUST re-register.')
r153 = RegistrationRule(
    rule='You must not have been declared incompetent for voting purposes by a probate court')
r154 = RegistrationRule(
    rule='You must not have been permanently denied the right to vote for violations of election laws.')
r155 = RegistrationRule(
    rule='You must be a citizen of the United States and a resident of the State of Oklahoma')
r156 = RegistrationRule(
    rule='You must be 18 years old on or before the date of the next election')
r157 = RegistrationRule(rule='You must be a "bona fide" resident of the State of Oklahoma (A person is a “bona fide” resident of the State of Oklahoma if he or she has an “honest intent to make a place one’s residence or domicile, a conscious decision to make a location an individual’s home.")')
r158 = RegistrationRule(
    rule='You must have not been convicted of a felony and not completed the sentence including any term of incarceration, parole or supervision, or probation')
r159 = RegistrationRule(
    rule='You must not now be under judgment as an incapacitated person, or a partially incapacitated person prohibited from voting')
r160 = RegistrationRule(rule='You must be a resident of Oregon')
r161 = RegistrationRule(
    rule='You must at least 16 years old (to vote, you must be 18 by Election Day)')
r162 = RegistrationRule(
    rule='You must be a citizen of the United States at least one month before the next election')
r163 = RegistrationRule(
    rule='You must be a resident of Pennsylvania and your election district at least 30 days before Election Day')
r164 = RegistrationRule(
    rule='You must be at least 18 years of age on the day of the next election')
r165 = RegistrationRule(
    rule='You must not be incarcerated after conviction for a felony (your voting rights are restored immediately after incarceration)')
r166 = RegistrationRule(
    rule='You must not have been convicted of violating any provision of the Pennsylvania Election Code within the last four years')
r167 = RegistrationRule(
    rule='You must be a resident of Rhode Island for 30 days preceding the next election')
r168 = RegistrationRule(
    rule='You must not be currently incarcerated in a correctional facility due to a felony conviction')
r169 = RegistrationRule(
    rule='You must not have been lawfully judged to be mentally incompetent')
r170 = RegistrationRule(
    rule='You must be a resident of South Carolina, and live in the county and precinct where you are registering')
r171 = RegistrationRule(
    rule='You must not be confined in any public prison resulting from a conviction of a crime')
r172 = RegistrationRule(rule='You must never have been convicted of a felony or offense against Election Day laws, or if previously convicted, have served your entire sentence, including probation or parole, or have received a pardon for the conviction')
r173 = RegistrationRule(
    rule='You must not be under a court order declaring you mentally incompetent')
r174 = RegistrationRule(rule='You must reside in South Dakota')
r175 = RegistrationRule(
    rule='You must not be currently serving a sentence for a felony conviction which included imprisonment, served or suspended, in an adult penitentiary system')
r176 = RegistrationRule(
    rule='You must not have been adjudged mentally incompetent by a court')
r177 = RegistrationRule(rule='You must be a resident of Tennessee')
r178 = RegistrationRule(
    rule='not have been convicted of a felony, or if convicted, have had your full rights of citizenship restored (or have received a pardon)')
r179 = RegistrationRule(
    rule='You must not be adjudicated incompetent by a court of competent jurisdiction (or have been restored to legal capacity')
r180 = RegistrationRule(
    rule='You must be a resident of the county in which the application for registration is made')
r181 = RegistrationRule(
    rule='You must be at least 17 years and 10 months old (you must be 18 to vote)')
r182 = RegistrationRule(
    rule='You must not be convicted of a felony, or if a convicted felon,')
r183 = RegistrationRule(
    rule='You must you must have fully discharged your punishment, including any incarceration, parole, supervision, period of probation, or be pardoned')
r184 = RegistrationRule(
    rule='You must have not been declared mentally incompetent by final judgment of a court of law')
r185 = RegistrationRule(
    rule='You must have resided in Utah for 30 days immediately before the next election')
r186 = RegistrationRule(rule='16- and 17-year-olds may preregister to vote, but cannot vote until they are 18 (Individuals may vote in a primary election if they are 17 years old on or before the date of the primary election and will be 18 years old on or before the date of the corresponding general election)')
r187 = RegistrationRule(
    rule='You must not be a convicted felon currently incarcerated for commission of a felony until your right to vote is restored')
r188 = RegistrationRule(
    rule='You must not be convicted of treason or crime against the elective franchise, unless restored to civil rights')
r189 = RegistrationRule(
    rule='You must not be found to be mentally incompetent by a court of law')
r190 = RegistrationRule(rule='You must be a resident of Vermont')
r191 = RegistrationRule(rule='You must be 18 years of age on or before Election Day (17 year olds who will be 18 years of age on or before the date of a general election may register and vote in the primary election immediately preceding that general election)')
r192 = RegistrationRule(
    rule='You must have taken the following Oath: You solemnly swear (or affirm) that whenever you give your vote or suffrage, touching any matter that concerns the state of Vermont, you will do it so as in your conscience you shall judge will most conduce to the best good of the same, as established by the Constitution, without fear or favor of any person [Voter’s Oath, Vermont Constitution, Chapter II, Section 42]')
r193 = RegistrationRule(
    rule='You must be a resident of Virginia and of the precinct in which you want to vote')
r194 = RegistrationRule(rule='You must be 18 years old by the next general election (a person who is 17 years old may register to vote in advance of his or her 18th birthday and can vote in intervening primary or special elections if the person will turn 18 by the date of the next general election)')
r195 = RegistrationRule(
    rule='You must not have been convicted of a felony, unless you have had your civil rights restored')
r196 = RegistrationRule(
    rule='You must not currently be declared incapacitated by a court')
r197 = RegistrationRule(
    rule='You must be at least 18 years old by Election Day')
r198 = RegistrationRule(
    rule='You must be a legal resident of Washington State, your county, and precinct for 30 days immediately preceding Election Day')
r199 = RegistrationRule(
    rule='You must not be disqualified from voting due to a court order')
r200 = RegistrationRule(
    rule='You must not be under Department of Corrections supervision for a Washington felony conviction')
r201 = RegistrationRule(
    rule='You must live in West Virginia in the county in which you are registering')
r202 = RegistrationRule(
    rule='You must be at least 17 years old and turning 18 before the next general election')
r203 = RegistrationRule(
    rule='You must not be under conviction, probation, or parole for a felony, treason, or election bribery')
r204 = RegistrationRule(
    rule='You must not have been judged “mentally incompetent” in a court of competent jurisdiction')
r205 = RegistrationRule(
    rule='You must be a resident of Wisconsin for at least 10 days')
r206 = RegistrationRule(rule='You must be 18 years old')
r207 = RegistrationRule(
    rule='You must not have been convicted of treason, felony or bribery, or if you have, your civil rights have been restored')
r208 = RegistrationRule(
    rule='You must not be incapable of understanding the objective of the elective process or under guardianship')
r209 = RegistrationRule(
    rule='You must be 18 years old by General Election Day')
r210 = RegistrationRule(rule='You must be a resident of the State of Wyoming')
r211 = RegistrationRule(
    rule='You must not be currently adjudicated mentally incompetent')
r212 = RegistrationRule(
    rule='You must not have been convicted of a felony, or if convicted have had your voting rights restored')


db.session.add_all([r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31, r32, r33, r34, r35, r36, r37, r38, r39, r40, r41, r42, r43, r44, r45, r46, r47, r48, r49, r50, r51, r52, r53, r54, r55, r56, r57, r58, r59, r60, r61, r62, r63, r64, r65, r66, r67, r68, r69, r70, r71, r72, r73, r74, r75, r76, r77, r78, r79, r80, r81, r82, r83, r84, r85, r86, r87, r88, r89, r90, r91, r92, r93, r94, r95, r96, r97, r98, r99, r100, r101, r101, r102, r103, r104, r105, r106, r107, r108, r109, r110, r111, r112, r113,
                   r114, r115, r116, r117, r118, r119, r120, r121, r122, r123, r124, r125, r126, r127, r128, r129, r130, r131, r132, r133, r134, r135, r136, r137, r138, r139, r140, r141, r142, r143, r144, r145, r146, r147, r148, r149, r150, r151, r152, r153, r154, r155, r156, r157, r158, r159, r160, r161, r162, r163, r164, r165, r166, r167, r168, r169, r170, r171, r172, r173, r174, r175, r176, r177, r178, r179, r180, r181, r182, r183, r184, r185, r186, r187, r188, r189, r190, r191, r192, r193, r194, r195, r196, r197, r198, r199, r200, r201, r202, r203, r204, r205, r206, r207, r208, r209, r210, r211, r212])
db.session.commit()

sr1 = StateRegistrationRule(state_id='AL', rule_id=1)
sr2 = StateRegistrationRule(state_id='AL', rule_id=2)
sr3 = StateRegistrationRule(state_id='AL', rule_id=3)
sr4 = StateRegistrationRule(state_id='AL', rule_id=4)
sr5 = StateRegistrationRule(state_id='AL', rule_id=5)
sr6 = StateRegistrationRule(state_id='AL', rule_id=6)
sr7 = StateRegistrationRule(state_id='AK', rule_id=1)
sr8 = StateRegistrationRule(state_id='AK', rule_id=7)
sr9 = StateRegistrationRule(state_id='AK', rule_id=8)
sr10 = StateRegistrationRule(state_id='AK', rule_id=9)
sr11 = StateRegistrationRule(state_id='AK', rule_id=10)
sr12 = StateRegistrationRule(state_id='AZ', rule_id=1)
sr13 = StateRegistrationRule(state_id='AZ', rule_id=11)
sr14 = StateRegistrationRule(state_id='AZ', rule_id=12)
sr15 = StateRegistrationRule(state_id='AZ', rule_id=13)
sr16 = StateRegistrationRule(state_id='AZ', rule_id=14)
sr17 = StateRegistrationRule(state_id='AZ', rule_id=15)
sr18 = StateRegistrationRule(state_id='AR', rule_id=1)
sr19 = StateRegistrationRule(state_id='AR', rule_id=16)
sr20 = StateRegistrationRule(state_id='AR', rule_id=17)
sr21 = StateRegistrationRule(state_id='AR', rule_id=18)
sr22 = StateRegistrationRule(state_id='AR', rule_id=19)
sr23 = StateRegistrationRule(state_id='AR', rule_id=20)
sr24 = StateRegistrationRule(state_id='CA', rule_id=1)
sr25 = StateRegistrationRule(state_id='CA', rule_id=21)
sr26 = StateRegistrationRule(state_id='CA', rule_id=22)
sr27 = StateRegistrationRule(state_id='CA', rule_id=23)
sr28 = StateRegistrationRule(state_id='CA', rule_id=24)
sr29 = StateRegistrationRule(state_id='CO', rule_id=1)
sr30 = StateRegistrationRule(state_id='CO', rule_id=25)
sr31 = StateRegistrationRule(state_id='CO', rule_id=26)
sr32 = StateRegistrationRule(state_id='CO', rule_id=27)
sr33 = StateRegistrationRule(state_id='CT', rule_id=1)
sr34 = StateRegistrationRule(state_id='CT', rule_id=28)
sr35 = StateRegistrationRule(state_id='CT', rule_id=29)
sr36 = StateRegistrationRule(state_id='CT', rule_id=30)
sr37 = StateRegistrationRule(state_id='DE', rule_id=1)
sr38 = StateRegistrationRule(state_id='DE', rule_id=31)
sr39 = StateRegistrationRule(state_id='DE', rule_id=32)
sr40 = StateRegistrationRule(state_id='DE', rule_id=33)
sr41 = StateRegistrationRule(state_id='DE', rule_id=34)
sr42 = StateRegistrationRule(state_id='DC', rule_id=1)
sr43 = StateRegistrationRule(state_id='DC', rule_id=35)
sr44 = StateRegistrationRule(state_id='DC', rule_id=36)
sr45 = StateRegistrationRule(state_id='DC', rule_id=37)
sr46 = StateRegistrationRule(state_id='DC', rule_id=38)
sr47 = StateRegistrationRule(state_id='DC', rule_id=39)
sr48 = StateRegistrationRule(state_id='FL', rule_id=1)
sr49 = StateRegistrationRule(state_id='FL', rule_id=40)
sr50 = StateRegistrationRule(state_id='FL', rule_id=41)
sr51 = StateRegistrationRule(state_id='FL', rule_id=42)
sr52 = StateRegistrationRule(state_id='FL', rule_id=43)
sr53 = StateRegistrationRule(state_id='FL', rule_id=44)
sr54 = StateRegistrationRule(state_id='GA', rule_id=1)
sr55 = StateRegistrationRule(state_id='GA', rule_id=45)
sr56 = StateRegistrationRule(state_id='GA', rule_id=46)
sr57 = StateRegistrationRule(state_id='GA', rule_id=47)
sr58 = StateRegistrationRule(state_id='GA', rule_id=48)
sr59 = StateRegistrationRule(state_id='HI', rule_id=1)
sr60 = StateRegistrationRule(state_id='HI', rule_id=49)
sr61 = StateRegistrationRule(state_id='HI', rule_id=50)
sr62 = StateRegistrationRule(state_id='HI', rule_id=51)
sr63 = StateRegistrationRule(state_id='HI', rule_id=52)
sr64 = StateRegistrationRule(state_id='ID', rule_id=53)
sr65 = StateRegistrationRule(state_id='ID', rule_id=1)
sr66 = StateRegistrationRule(state_id='ID', rule_id=54)
sr67 = StateRegistrationRule(state_id='ID', rule_id=55)
sr68 = StateRegistrationRule(state_id='IL', rule_id=1)
sr69 = StateRegistrationRule(state_id='IL', rule_id=56)
sr70 = StateRegistrationRule(state_id='IL', rule_id=57)
sr71 = StateRegistrationRule(state_id='IL', rule_id=58)
sr72 = StateRegistrationRule(state_id='IL', rule_id=59)
sr73 = StateRegistrationRule(state_id='IN', rule_id=1)
sr74 = StateRegistrationRule(state_id='IN', rule_id=60)
sr75 = StateRegistrationRule(state_id='IN', rule_id=61)
sr76 = StateRegistrationRule(state_id='IN', rule_id=62)
sr77 = StateRegistrationRule(state_id='IA', rule_id=1)
sr78 = StateRegistrationRule(state_id='IA', rule_id=63)
sr79 = StateRegistrationRule(state_id='IA', rule_id=64)
sr80 = StateRegistrationRule(state_id='IA', rule_id=65)
sr81 = StateRegistrationRule(state_id='IA', rule_id=66)
sr82 = StateRegistrationRule(state_id='IA', rule_id=67)
sr83 = StateRegistrationRule(state_id='KS', rule_id=1)
sr84 = StateRegistrationRule(state_id='KS', rule_id=68)
sr85 = StateRegistrationRule(state_id='KS', rule_id=69)
sr86 = StateRegistrationRule(state_id='KS', rule_id=70)
sr87 = StateRegistrationRule(state_id='KS', rule_id=71)
sr88 = StateRegistrationRule(state_id='KY', rule_id=1)
sr89 = StateRegistrationRule(state_id='KY', rule_id=72)
sr90 = StateRegistrationRule(state_id='KY', rule_id=73)
sr91 = StateRegistrationRule(state_id='KY', rule_id=74)
sr92 = StateRegistrationRule(state_id='KY', rule_id=75)
sr93 = StateRegistrationRule(state_id='KY', rule_id=76)
sr94 = StateRegistrationRule(state_id='LA', rule_id=1)
sr95 = StateRegistrationRule(state_id='LA', rule_id=77)
sr96 = StateRegistrationRule(state_id='LA', rule_id=78)
sr97 = StateRegistrationRule(state_id='LA', rule_id=79)
sr98 = StateRegistrationRule(state_id='LA', rule_id=80)
sr99 = StateRegistrationRule(state_id='ME', rule_id=1)
sr100 = StateRegistrationRule(state_id='ME', rule_id=81)
sr101 = StateRegistrationRule(state_id='ME', rule_id=82)
sr102 = StateRegistrationRule(state_id='MD', rule_id=1)
sr103 = StateRegistrationRule(state_id='MD', rule_id=83)
sr104 = StateRegistrationRule(state_id='MD', rule_id=84)
sr105 = StateRegistrationRule(state_id='MD', rule_id=85)
sr106 = StateRegistrationRule(state_id='MD', rule_id=86)
sr107 = StateRegistrationRule(state_id='MD', rule_id=87)
sr108 = StateRegistrationRule(state_id='MA', rule_id=1)
sr109 = StateRegistrationRule(state_id='MA', rule_id=88)
sr110 = StateRegistrationRule(state_id='MA', rule_id=89)
sr111 = StateRegistrationRule(state_id='MA', rule_id=90)
sr112 = StateRegistrationRule(state_id='MA', rule_id=91)
sr113 = StateRegistrationRule(state_id='MA', rule_id=92)
sr114 = StateRegistrationRule(state_id='MI', rule_id=1)
sr115 = StateRegistrationRule(state_id='MI', rule_id=93)
sr116 = StateRegistrationRule(state_id='MI', rule_id=94)
sr117 = StateRegistrationRule(state_id='MI', rule_id=95)
sr118 = StateRegistrationRule(state_id='MN', rule_id=1)
sr119 = StateRegistrationRule(state_id='MN', rule_id=96)
sr120 = StateRegistrationRule(state_id='MN', rule_id=97)
sr121 = StateRegistrationRule(state_id='MN', rule_id=98)
sr122 = StateRegistrationRule(state_id='MN', rule_id=99)
sr123 = StateRegistrationRule(state_id='MN', rule_id=100)
sr124 = StateRegistrationRule(state_id='MN', rule_id=101)
sr125 = StateRegistrationRule(state_id='MS', rule_id=1)
sr126 = StateRegistrationRule(state_id='MS', rule_id=102)
sr127 = StateRegistrationRule(state_id='MS', rule_id=103)
sr128 = StateRegistrationRule(state_id='MS', rule_id=104)
sr129 = StateRegistrationRule(state_id='MS', rule_id=105)
sr130 = StateRegistrationRule(state_id='MO', rule_id=1)
sr131 = StateRegistrationRule(state_id='MO', rule_id=106)
sr132 = StateRegistrationRule(state_id='MO', rule_id=107)
sr133 = StateRegistrationRule(state_id='MO', rule_id=108)
sr134 = StateRegistrationRule(state_id='MO', rule_id=109)
sr135 = StateRegistrationRule(state_id='MO', rule_id=110)
sr136 = StateRegistrationRule(state_id='MO', rule_id=111)
sr137 = StateRegistrationRule(state_id='MT', rule_id=1)
sr138 = StateRegistrationRule(state_id='MT', rule_id=112)
sr139 = StateRegistrationRule(state_id='MT', rule_id=113)
sr140 = StateRegistrationRule(state_id='MT', rule_id=114)
sr141 = StateRegistrationRule(state_id='MT', rule_id=115)
sr142 = StateRegistrationRule(state_id='MT', rule_id=116)
sr143 = StateRegistrationRule(state_id='NE', rule_id=1)
sr144 = StateRegistrationRule(state_id='NE', rule_id=117)
sr145 = StateRegistrationRule(state_id='NE', rule_id=118)
sr146 = StateRegistrationRule(state_id='NE', rule_id=119)
sr147 = StateRegistrationRule(state_id='NE', rule_id=120)
sr148 = StateRegistrationRule(state_id='NE', rule_id=121)
sr149 = StateRegistrationRule(state_id='NV', rule_id=1)
sr150 = StateRegistrationRule(state_id='NV', rule_id=122)
sr151 = StateRegistrationRule(state_id='NV', rule_id=123)
sr152 = StateRegistrationRule(state_id='NV', rule_id=124)
sr153 = StateRegistrationRule(state_id='NV', rule_id=125)
sr154 = StateRegistrationRule(state_id='NV', rule_id=126)
sr155 = StateRegistrationRule(state_id='NH', rule_id=1)
sr156 = StateRegistrationRule(state_id='NH', rule_id=127)
sr157 = StateRegistrationRule(state_id='NH', rule_id=128)
sr158 = StateRegistrationRule(state_id='NH', rule_id=129)
sr159 = StateRegistrationRule(state_id='NH', rule_id=130)
sr160 = StateRegistrationRule(state_id='NJ', rule_id=1)
sr161 = StateRegistrationRule(state_id='NJ', rule_id=131)
sr162 = StateRegistrationRule(state_id='NJ', rule_id=132)
sr163 = StateRegistrationRule(state_id='NJ', rule_id=133)
sr164 = StateRegistrationRule(state_id='NJ', rule_id=134)
sr165 = StateRegistrationRule(state_id='NM', rule_id=1)
sr166 = StateRegistrationRule(state_id='NM', rule_id=135)
sr167 = StateRegistrationRule(state_id='NM', rule_id=136)
sr168 = StateRegistrationRule(state_id='NM', rule_id=137)
sr169 = StateRegistrationRule(state_id='NM', rule_id=138)
sr170 = StateRegistrationRule(state_id='NY', rule_id=1)
sr171 = StateRegistrationRule(state_id='NY', rule_id=139)
sr172 = StateRegistrationRule(state_id='NY', rule_id=140)
sr173 = StateRegistrationRule(state_id='NY', rule_id=141)
sr174 = StateRegistrationRule(state_id='NY', rule_id=142)
sr175 = StateRegistrationRule(state_id='NY', rule_id=143)
sr176 = StateRegistrationRule(state_id='NC', rule_id=1)
sr177 = StateRegistrationRule(state_id='NC', rule_id=144)
sr178 = StateRegistrationRule(state_id='NC', rule_id=145)
sr179 = StateRegistrationRule(state_id='NC', rule_id=146)
sr180 = StateRegistrationRule(state_id='ND', rule_id=1)
sr181 = StateRegistrationRule(state_id='ND', rule_id=147)
sr182 = StateRegistrationRule(state_id='ND', rule_id=148)
sr183 = StateRegistrationRule(state_id='ND', rule_id=149)
sr184 = StateRegistrationRule(state_id='OH', rule_id=1)
sr185 = StateRegistrationRule(state_id='OH', rule_id=150)
sr186 = StateRegistrationRule(state_id='OH', rule_id=151)
sr187 = StateRegistrationRule(state_id='OH', rule_id=152)
sr188 = StateRegistrationRule(state_id='OH', rule_id=153)
sr189 = StateRegistrationRule(state_id='OH', rule_id=154)
sr190 = StateRegistrationRule(state_id='OK', rule_id=155)
sr191 = StateRegistrationRule(state_id='OK', rule_id=156)
sr192 = StateRegistrationRule(state_id='OK', rule_id=157)
sr193 = StateRegistrationRule(state_id='OK', rule_id=158)
sr194 = StateRegistrationRule(state_id='OK', rule_id=159)
sr195 = StateRegistrationRule(state_id='OR', rule_id=1)
sr196 = StateRegistrationRule(state_id='OR', rule_id=160)
sr197 = StateRegistrationRule(state_id='OR', rule_id=161)
sr198 = StateRegistrationRule(state_id='PA', rule_id=162)
sr199 = StateRegistrationRule(state_id='PA', rule_id=163)
sr200 = StateRegistrationRule(state_id='PA', rule_id=164)
sr201 = StateRegistrationRule(state_id='PA', rule_id=165)
sr202 = StateRegistrationRule(state_id='PA', rule_id=166)
sr203 = StateRegistrationRule(state_id='RI', rule_id=1)
sr204 = StateRegistrationRule(state_id='RI', rule_id=167)
sr205 = StateRegistrationRule(state_id='RI', rule_id=140)
sr206 = StateRegistrationRule(state_id='RI', rule_id=168)
sr207 = StateRegistrationRule(state_id='RI', rule_id=169)
sr208 = StateRegistrationRule(state_id='SC', rule_id=1)
sr209 = StateRegistrationRule(state_id='SC', rule_id=57)
sr210 = StateRegistrationRule(state_id='SC', rule_id=170)
sr211 = StateRegistrationRule(state_id='SC', rule_id=171)
sr212 = StateRegistrationRule(state_id='SC', rule_id=172)
sr213 = StateRegistrationRule(state_id='SC', rule_id=173)
sr214 = StateRegistrationRule(state_id='SD', rule_id=1)
sr215 = StateRegistrationRule(state_id='SD', rule_id=174)
sr216 = StateRegistrationRule(state_id='SD', rule_id=93)
sr217 = StateRegistrationRule(state_id='SD', rule_id=175)
sr218 = StateRegistrationRule(state_id='SD', rule_id=176)
sr219 = StateRegistrationRule(state_id='TN', rule_id=1)
sr220 = StateRegistrationRule(state_id='TN', rule_id=177)
sr221 = StateRegistrationRule(state_id='TN', rule_id=57)
sr222 = StateRegistrationRule(state_id='TN', rule_id=178)
sr223 = StateRegistrationRule(state_id='TN', rule_id=179)
sr224 = StateRegistrationRule(state_id='TX', rule_id=1)
sr225 = StateRegistrationRule(state_id='TX', rule_id=180)
sr226 = StateRegistrationRule(state_id='TX', rule_id=181)
sr227 = StateRegistrationRule(state_id='TX', rule_id=182)
sr228 = StateRegistrationRule(state_id='TX', rule_id=183)
sr229 = StateRegistrationRule(state_id='TX', rule_id=184)
sr230 = StateRegistrationRule(state_id='UT', rule_id=1)
sr231 = StateRegistrationRule(state_id='UT', rule_id=185)
sr232 = StateRegistrationRule(state_id='UT', rule_id=186)
sr233 = StateRegistrationRule(state_id='UT', rule_id=187)
sr234 = StateRegistrationRule(state_id='UT', rule_id=188)
sr235 = StateRegistrationRule(state_id='UT', rule_id=189)
sr236 = StateRegistrationRule(state_id='VT', rule_id=1)
sr237 = StateRegistrationRule(state_id='VT', rule_id=190)
sr238 = StateRegistrationRule(state_id='VT', rule_id=191)
sr239 = StateRegistrationRule(state_id='VT', rule_id=192)
sr240 = StateRegistrationRule(state_id='VA', rule_id=1)
sr241 = StateRegistrationRule(state_id='VA', rule_id=193)
sr242 = StateRegistrationRule(state_id='VA', rule_id=194)
sr243 = StateRegistrationRule(state_id='VA', rule_id=195)
sr244 = StateRegistrationRule(state_id='VA', rule_id=196)
sr245 = StateRegistrationRule(state_id='WA', rule_id=1)
sr246 = StateRegistrationRule(state_id='WA', rule_id=197)
sr247 = StateRegistrationRule(state_id='WA', rule_id=198)
sr248 = StateRegistrationRule(state_id='WA', rule_id=199)
sr249 = StateRegistrationRule(state_id='WA', rule_id=200)
sr250 = StateRegistrationRule(state_id='WV', rule_id=1)
sr251 = StateRegistrationRule(state_id='WV', rule_id=201)
sr252 = StateRegistrationRule(state_id='WV', rule_id=202)
sr253 = StateRegistrationRule(state_id='WV', rule_id=203)
sr254 = StateRegistrationRule(state_id='WV', rule_id=204)
sr255 = StateRegistrationRule(state_id='WI', rule_id=1)
sr256 = StateRegistrationRule(state_id='WI', rule_id=205)
sr257 = StateRegistrationRule(state_id='WI', rule_id=206)
sr258 = StateRegistrationRule(state_id='WI', rule_id=207)
sr259 = StateRegistrationRule(state_id='WI', rule_id=208)
sr260 = StateRegistrationRule(state_id='WY', rule_id=1)
sr261 = StateRegistrationRule(state_id='WY', rule_id=209)
sr262 = StateRegistrationRule(state_id='WY', rule_id=210)
sr263 = StateRegistrationRule(state_id='WY', rule_id=211)
sr264 = StateRegistrationRule(state_id='WY', rule_id=212)

db.session.add_all([sr1, sr2, sr3, sr4, sr5, sr6, sr7, sr8, sr9, sr10, sr11, sr12, sr13, sr14, sr15, sr16, sr17, sr18, sr19, sr20, sr21, sr22, sr23, sr24, sr25, sr26, sr27, sr28, sr29, sr30, sr31, sr32, sr33, sr34, sr35, sr36, sr37, sr38, sr39, sr40, sr41, sr42, sr43, sr44, sr45, sr46, sr47, sr48, sr49, sr50, sr51, sr52, sr53, sr54, sr55, sr56, sr57, sr58, sr59, sr60, sr61, sr62, sr63, sr64, sr65, sr66, sr67, sr68, sr69, sr70, sr71, sr72, sr73, sr74, sr75, sr76, sr77, sr78, sr79, sr80, sr81, sr82, sr83, sr84, sr85, sr86, sr87, sr88, sr89, sr90, sr91, sr92, sr93, sr94, sr95, sr96, sr97, sr98, sr99, sr100, sr101, sr101, sr102, sr103, sr104, sr105, sr106, sr107, sr108, sr109, sr110, sr111, sr112, sr113, sr114, sr115, sr116, sr117, sr118, sr119, sr120, sr121, sr122, sr123, sr124, sr125, sr126, sr127, sr128, sr129, sr130, sr131, sr132, sr133, sr134, sr135, sr136, sr137, sr138,
                   sr139, sr140, sr141, sr142, sr143, sr144, sr145, sr146, sr147, sr148, sr149, sr150, sr151, sr152, sr153, sr154, sr155, sr156, sr157, sr158, sr159, sr160, sr161, sr162, sr163, sr164, sr165, sr166, sr167, sr168, sr169, sr170, sr171, sr172, sr173, sr174, sr175, sr176, sr177, sr178, sr179, sr180, sr181, sr182, sr183, sr184, sr185, sr186, sr187, sr188, sr189, sr190, sr191, sr192, sr193, sr194, sr195, sr196, sr197, sr198, sr199, sr200, sr201, sr202, sr203, sr204, sr205, sr206, sr207, sr208, sr209, sr210, sr211, sr212, sr213, sr214, sr215, sr216, sr217, sr218, sr219, sr220, sr221, sr222, sr223, sr224, sr225, sr226, sr227, sr228, sr229, sr230, sr231, sr232, sr233, sr234, sr235, sr236, sr237, sr238, sr239, sr240, sr241, sr242, sr243, sr244, sr245, sr246, sr247, sr248, sr249, sr250, sr251, sr252, sr253, sr254, sr255, sr256, sr257, sr258, sr259, sr260, sr261, sr262, sr263, sr264])
db.session.commit()

e1 = Election(name='House District 63 - Special Primary Election (will not be held but this date is deadline for submission of independent candidate and minor party ballot access petitions)', date='2021-10-19', state_id='AL')
e2 = Election(name='State House District 76 - Special Primary Election',
                   date='2021-11-16', state_id='AL')
e3 = Election(name='State House District 76 - Special Primary Runoff Election (if necessary)',
                   date='2021-12-14', state_id='AL')
e4 = Election(name='	State House District 76 - Special General Election',
                   date='2022-03-01', state_id='AL')
e5 = Election(name='2022 Primary Election',
                   date='2022-05-24', state_id='AL')
e6 = Election(name='2022 Primary Runoff Election',
                   date='2022-06-21', state_id='AL')
e7 = Election(name='2022 General Election',
                   date='2022-11-08', state_id='AL')

db.session.add_all([e1, e2, e3, e4, e5, e6, e7])
db.session.commit()

e1 = Election(name='Regional Educational Attendance Area (REAA) Election - Polls open 8am to 8pm.',
                   date='2022-10-05', state_id='AK')
e2 = Election(name='2022 Primary Election',
                   date='2022-08-16', state_id='AK')
e3 = Election(name='2022 General Election',
                   date='2022-11-08', state_id='AK')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Election For Select Local Jurisdictions',
                   date='2021-11-02', state_id='AZ')
e2 = Election(name='Election For Select Local Jurisdictions',
                   date='2022-03-08', state_id='AZ')
e3 = Election(name='Election For Select Local Jurisdictions',
                   date='2022-05-17', state_id='AZ')
e4 = Election(name='State Primary Election',
                   date='2022-08-02', state_id='AZ')
e5 = Election(name='State General Election',
                   date='2022-11-08', state_id='AZ')

db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()


e1 = Election(name='State Primary Election', date='2022-05-24', state_id='AR')
e2 = Election(name='State General Election', date='2022-11-08', state_id='AR')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='California Gubernatorial Recall Election',
              date='2021-09-14', state_id='CA')
e2 = Election(name='Statewide Direct Primary Election',
              date='2022-06-07', state_id='CA')
e3 = Election(name='State General Election', date='2022-11-08', state_id='CA')
e4 = Election(name='Local Election - Bear Valley Water District, Kirkwood Meadows Public Utility District, Markleeville Utility District',
              date='2021-11-02', state_id='CA')
e5 = Election(name='Local Election - UDEL', date='2021-11-02', state_id='CA')
e6 = Election(name='Special District Election - Colusa',
              date='2021-11-02', state_id='CA')
e7 = Election(name='Lassen College Trustee Area 1 Election',
              date='2021-09-14', state_id='CA')
e8 = Election(name='City of Vernon Special Municipal Election',
              date='2021-09-14', state_id='CA')
e9 = Election(name='Los Angeles Local and Municipal Election',
              date='2021-11-02', state_id='CA')
e10 = Election(name='Merced Special Vacancy Mail Ballot Election Los Banos Unified School District Area 1',
               date='2021-11-02', state_id='CA')
e11 = Election(name='Monterey - Chualar Union School District Trustee Area 1 Governing Board Member Special Election',
               date='2021-11-02', state_id='CA')
e12 = Election(name='Long Valley Community Services District Election',
               date='2021-11-02', state_id='CA')
e13 = Election(name='Sacramento - SCERS Election',
               date='2021-10-01', state_id='CA')
e14 = Election(name='City of Isleton Fire Protection Services Transaction and Use Tax Special Election',
               date='2021-11-02', state_id='CA')
e15 = Election(name='San Bernardino City Employees’ Retirement Association Election',
               date='2021-12-07', state_id='CA')
e16 = Election(name='San Mateo Special Election',
               date='2021-11-02', state_id='CA')
e17 = Election(name='City of Santa Barbara Municipal Election',
               date='2021-11-02', state_id='CA')
e18 = Election(name='Live Oak City Vacancy Election',
               date='2021-12-07', state_id='CA')
e19 = Election(name='Tulare County Employee’s Retirement Association Election',
               date='2021-12-07', state_id='CA')
e20 = Election(name='City of Oxnard District 2, Special Vacancy Election',
               date='2021-11-02', state_id='CA')
db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10,
                   e11, e12, e13, e14, e15, e16, e17, e18, e19, e20])
db.session.commit()

e1 = Election(name='Statewide Election - Ballot Measures - Polls open 7:00am to 7:00pm',
              date='2021-11-02', state_id='CO')
e2 = Election(name='Republican Party Precinct Caucus Day',
              date='2022-03-01', state_id='CO')
e3 = Election(name='Democratic Party Precinct Caucus Day',
              date='2022-03-01', state_id='CO')
e4 = Election(name='State Primary Election', date='2022-06-08', state_id='CO')
e5 = Election(name='State General Election', date='2022-11-08', state_id='CO')

db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()

e1 = Election(name='Statewide Election', date='2021-11-02', state_id='CT')
e2 = Election(name='State Primary Election', date='2022-08-09', state_id='CT')
e3 = Election(name='State General Election', date='2022-11-08', state_id='CT')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Election - Town of Dewey Beach',
              date='2021-09-18', state_id='DE')
e2 = Election(name='Election - Town of Dagsboro',
              date='2021-12-04', state_id='DE')
e3 = Election(name='State Primary Election', date='2022-09-08', state_id='DE')
e4 = Election(name='State General Election', date='2022-11-08', state_id='DE')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='District of Columbia - General Election',
              date='2022-11-08', state_id='DC')
db.session.add(e1)
db.session.commit()

e1 = Election(name='Florida - City of Ocala Election',
              date='2021-09-21', state_id='FL')
e2 = Election(name='Special Primary Election - U.S. House of Representatives District 20',
              date='2021-11-02', state_id='FL')
e3 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='FL')
e4 = Election(name='Special General Election - U.S. House of Representatives District 20',
              date='2022-01-11', state_id='FL')
e5 = Election(name='State Primary Election', date='2022-08-23', state_id='FL')
e6 = Election(name='State General Election', date='2022-11-08', state_id='FL')
db.session.add_all([e1, e2, e3, e4, e5, e6])
db.session.commit()

e1 = Election(name='Special Election', date='2021-09-21', state_id='GA')
e2 = Election(name='Special Election Runoff', date='2021-10-19', state_id='GA')
e3 = Election(name='General Election/Special Election',
              date='2021-11-02', state_id='GA')
e4 = Election(name='General Election/Special Election Runoff',
              date='2021-11-30', state_id='GA')
e5 = Election(name='State Primary Election', date='2022-05-24', state_id='GA')
e6 = Election(name='State Primary Runoff', date='2022-06-26', state_id='GA')
e7 = Election(name='State General Election', date='2022-11-08', state_id='GA')
e8 = Election(name='State Runoff Election', date='2022-12-06', state_id='GA')
e9 = Election(name='Federal Runoff Election', date='2023-01-10', state_id='GA')
db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9])
db.session.commit()

e1 = Election(name='State Primary Election', date='2022-08-13', state_id='HI')
e2 = Election(name='State General Election', date='2022-11-08', state_id='HI')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='ID')
e2 = Election(name='City Runoff Elections', date='2021-12-02', state_id='ID')
e3 = Election(name='State Primary Election',
              date='2022-05-19', state_id='ID')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='ID')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='State Primary Election', date='2022-06-28', state_id='IL')
e2 = Election(name='State General Election', date='2022-11-08', state_id='IL')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='IN')
e2 = Election(name='State Primary Election', date='2022-05-03', state_id='IN')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='IN')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='City Primary Elections', date='2021-10-05', state_id='IA')
e2 = Election(name='Regular City and Regular School Election',
              date='2021-11-02', state_id='IA')
e3 = Election(name='City Runoff Elections',
              date='2021-11-30', state_id='IA')
e4 = Election(name='State Primary Election',
              date='2022-06-07', state_id='IA')
e5 = Election(name='State General Election', date='2022-11-08', state_id='IA')
db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()

e1 = Election(name='Kansas Municipal General Election',
              date='2021-11-02', state_id='KS')
e2 = Election(name='State Primary Election',
              date='2022-08-02', state_id='KS')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='KS')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='State Primary Election',
              date='2022-05-17', state_id='KY')
e2 = Election(name='State General Election',
              date='2022-11-08', state_id='KY')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Open Primary/Orleans Municipal Parochial Primary Election',
              date='2021-11-13', state_id='LA')
e2 = Election(name='Open Primary/Orleans Municipal Parochial General Election',
              date='2021-12-11', state_id='LA')
e3 = Election(name='Municipal Primary Election',
              date='2022-03-26', state_id='LA')
e4 = Election(name='Municipal General Election',
              date='2022-04-30', state_id='LA')
e5 = Election(name='State Primary Election',
              date='2022-11-08', state_id='LA')
e6 = Election(name='State General Election',
              date='2022-12-10', state_id='LA')
db.session.add_all([e1, e2, e3, e4, e5, e6])
db.session.commit()

e1 = Election(name='Maine Referendum Election',
              date='2021-11-02', state_id='ME')
e2 = Election(name='Maine Special Election for State Representative District 86',
              date='2021-11-02', state_id='ME')
e3 = Election(name='State Primary Election',
              date='2022-06-14', state_id='ME')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='ME')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Maryland Municipal General Election',
              date='2021-11-02', state_id='MD')
e2 = Election(name='State Primary Election',
              date='2022-06-28', state_id='MD')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='MD')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Massachusetts Preliminary Municipal Election',
              date='2021-09-14', state_id='MA')
e2 = Election(name='Massachusetts Municipal Election',
              date='2021-11-02', state_id='MA')
e3 = Election(name='State Primary Election',
              date='2022-09-20', state_id='MA')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='MA')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()


e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='MI')
e2 = Election(name='State Primary Election',
              date='2022-08-02', state_id='MI')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='MI')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='MN')
e2 = Election(name='Minnesota Precinct Caucus',
              date='2022-02-01', state_id='MN')
e3 = Election(name='Minnesota March Township Election',
              date='2021-03-08', state_id='MN')
e4 = Election(name='State Primary Election',
              date='2022-08-09', state_id='MN')
e5 = Election(name='State General Election',
              date='2022-11-08', state_id='MN')
db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='MS')
e2 = Election(name='Statewide General/Special Runoff Election',
              date='2021-12-23', state_id='MS')
e3 = Election(name='State Primary Election',
              date='2022-06-07', state_id='MS')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='MS')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='MO')
e2 = Election(name='Bond Elections',
              date='2022-02-08', state_id='MO')
e3 = Election(name='Charter City and Charter Counties Elections',
              date='2022-03-08', state_id='MO')
e4 = Election(name='General Municipal Election Day',
              date='2022-04-05', state_id='MO')
e5 = Election(name='State Primary Election',
              date='2022-07-06', state_id='MO')
e6 = Election(name='State General Election',
              date='2022-11-08', state_id='MO')
db.session.add_all([e1, e2, e3, e4, e5, e6])
db.session.commit()

e1 = Election(name='Municipal General Election',
              date='2021-11-02', state_id='MT')
e2 = Election(name='State Primary Election',
              date='2022-06-07', state_id='MT')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='MT')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='State Primary Election',
              date='2022-05-10', state_id='NE')
e2 = Election(name='State General Election',
              date='2022-11-08', state_id='NE')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='State Primary Election',
              date='2022-06-14', state_id='NV')
e2 = Election(name='State General Election',
              date='2022-11-08', state_id='NV')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Rockingham County District 6 (Derry) Primary Election',
              date='2021-10-19', state_id='NH')
e2 = Election(name='Cheshire County District 9 Special Election',
              date='2021-10-26', state_id='NH')
e3 = Election(name='Rockingham County District 6 (Derry) Special Election',
              date='2021-12-07', state_id='NH')
e4 = Election(name='State Primary Election',
              date='2022-09-13', state_id='NH')
e5 = Election(name='State General Election',
              date='2022-11-08', state_id='NH')
db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='NJ')
e2 = Election(name='State Primary Election',
              date='2022-06-07', state_id='NJ')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='NJ')
db.session.add_all([e1, e2, e3])
db.session.commit()


e1 = Election(name='New Mexico Regular Local Elections',
              date='2021-11-02', state_id='NM')
e2 = Election(name='New Mexico Municipal Officer Election',
              date='2022-03-01', state_id='NM')
e3 = Election(name='State Primary Election',
              date='2022-06-07', state_id='NM')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='NM')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='NY')
e2 = Election(name='State Primary Election',
              date='2022-06-28', state_id='NY')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='NY')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='North Carolina October Municipal Election',
              date='2021-10-05', state_id='NC')
e2 = Election(name='North Carolina November Municipal Election',
              date='2021-11-02', state_id='NC')
e3 = Election(name='State Primary Election',
              date='2022-03-08', state_id='NC')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='NC')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='North Dakota Township Elections',
              date='2022-03-15', state_id='ND')
e2 = Election(name='North Dakota City Elections',
              date='2022-06-14', state_id='ND')
e3 = Election(name='State Primary Election',
              date='2022-06-14', state_id='ND')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='ND')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='OH')
e2 = Election(name='State Primary Election',
              date='2022-05-03', state_id='OH')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='OH')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Oklahoma Special Election - Special Candidate and Propositions',
              date='2021-09-14', state_id='OK')
e2 = Election(name='Oklahoma Special Election - Special Proposition Election',
              date='2021-10-12', state_id='OK')
e3 = Election(name='Oklahoma Special Election - Special Candidate and Propositions',
              date='2021-11-09', state_id='OK')
e4 = Election(name='Oklahoma Special Election - Spcial Proposition',
              date='2021-12-14', state_id='OK')
e5 = Election(name='Oklahoma Board of Education Primary Special Elections',
              date='2022-02-08', state_id='OK')
e6 = Election(name='Oklahoma Board of Education General Special Elections',
              date='2022-04-05', state_id='OK')
e7 = Election(name='State Primary Election',
              date='2022-06-28', state_id='OK')
e8 = Election(name='State Primary Runoff',
              date='2022-08-23', state_id='OK')
e9 = Election(name='State General Election',
              date='2022-11-08', state_id='OK')
db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9])
db.session.commit()

e1 = Election(name='Statewide Municipal Election',
              date='2021-09-21', state_id='OR')
e2 = Election(name='Statewide Municipal Election',
              date='2021-11-02', state_id='OR')
e3 = Election(name='State Primary Election',
              date='2022-05-17', state_id='OR')
e4 = Election(name='State General Election',
              date='2022-11-08', state_id='OR')

db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='PA')
e2 = Election(name='State Primary Election',
              date='2022-05-17', state_id='PA')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='PA')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='State Primary Election',
              date='2022-09-13', state_id='RI')
e2 = Election(name='State Primary Runoff',
              date='2022-09-24', state_id='RI')
e3 = Election(name='State General Election',
              date='2022-11-08', state_id='RI')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='South Carolina - City of Orangeburg General Election',
              date='2021-09-14', state_id='SC')
e2 = Election(name='South Carolina - Laurens County Council District 3 Election',
              date='2021-09-21', state_id='SC')
e3 = Election(name='South Carolina - Town of Blenheim Special Election',
              date='2021-10-05', state_id='SC')
e4 = Election(name='South Carolina - Rich/Lex School Board District 5 Special Election',
              date='2021-10-12', state_id='SC')
e5 = Election(name='South Carolina - City of Rock Hill General Election',
              date='2021-10-19', state_id='SC')
e6 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='SC')
e7 = Election(name='South Carolina - Greenwood County Council Spec Election',
              date='2021-12-28', state_id='SC')
e8 = Election(name='State Primary Election', date='2022-06-14', state_id='SC')
e9 = Election(name='State Primary Runoff', date='2022-06-28', state_id='SC')
e10 = Election(name='State General Election', date='2022-11-08', state_id='SC')
db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9, e10])
db.session.commit()

e1 = Election(name='State Primary Election',
              date='2022-06-07', state_id='SD')
e2 = Election(name='State General Election',
              date='2022-11-08', state_id='SD')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Tennessee - City of Dickson Election',
              date='2021-09-23', state_id='TN')
e2 = Election(name='Tennessee - Town of Centerville Election',
              date='2021-10-02', state_id='TN')
e3 = Election(name='Tennessee - City of Franklin Election',
              date='2021-10-26', state_id='TN')
e4 = Election(name='Statewide Municipal Elections',
              date='2021-11-02', state_id='TN')
e5 = Election(name='Tennessee - Town of Ashland City Election',
              date='2021-12-04', state_id='TN')
e6 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='TN')
e7 = Election(name='State and County Primary Election',
              date='2022-05-03', state_id='TN')
e8 = Election(name='State Primary Election', date='2022-08-04', state_id='TN')
e9 = Election(name='State General Election', date='2022-11-08', state_id='TN')
db.session.add_all([e1, e2, e3, e4, e5, e6, e7, e8, e9])
db.session.commit()

e1 = Election(name='Texas - Uniform Election',
              date='2021-11-02', state_id='TX')
e2 = Election(name='State Primary Election', date='2022-03-01', state_id='TX')
e3 = Election(name='Texas - Uniform Election',
              date='2022-05-07', state_id='TX')
e4 = Election(name='Texas - Runoff Election',
              date='2022-05-24', state_id='TX')
e5 = Election(name='State General Election', date='2022-11-08', state_id='TX')
db.session.add_all([e1, e2, e3, e4, e5])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='UT')
e2 = Election(name='State Primary Election', date='2022-06-28', state_id='UT')
e3 = Election(name='State General Election', date='2022-11-08', state_id='UT')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='State Primary Election', date='2022-08-09', state_id='VT')
e2 = Election(name='State General Election', date='2022-11-08', state_id='VT')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='VA')
e3 = Election(name='Statewide General Election',
              date='2022-05-03', state_id='VA')
e3 = Election(name='State Primary Election', date='2022-06-21', state_id='VA')
e4 = Election(name='State General Election', date='2022-11-08', state_id='VA')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()

e1 = Election(name='Statewide General Election',
              date='2021-11-02', state_id='WA')
e2 = Election(name='State Primary Election', date='2022-08-02', state_id='WA')
e3 = Election(name='State General Election', date='2022-11-08', state_id='WA')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='State Primary Election', date='2022-05-10', state_id='WV')
e2 = Election(name='State General Election', date='2022-11-08', state_id='WV')
db.session.add_all([e1, e2])
db.session.commit()

e1 = Election(name='Wisconsin - Spring Election',
              date='2022-04-05', state_id='WI')
e2 = Election(name='State Primary Election', date='2022-08-09', state_id='WI')
e3 = Election(name='State General Election', date='2022-11-08', state_id='WI')
db.session.add_all([e1, e2, e3])
db.session.commit()

e1 = Election(name='Wyoming - Special Election',
              date='2022-03-22', state_id='WY')
e2 = Election(name='Wyoming - Town Elections',
              date='2022-05-03', state_id='WY')
e3 = Election(name='State Primary Election', date='2022-08-16', state_id='WY')
e4 = Election(name='State General Election', date='2022-11-08', state_id='WY')
db.session.add_all([e1, e2, e3, e4])
db.session.commit()
