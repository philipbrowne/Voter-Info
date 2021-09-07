from models import db, State, User
from app import app

db.drop_all()
db.create_all()

AL = State(id='AL', name='Alabama', capital='Montgomery', registration_url='https://www.sos.alabama.gov/alabama-votes/voter/register-to-vote?ref=voteusa',
           elections_url='https://www.sos.alabama.gov/alabama-votes/voter/upcoming-elections')
AK = State(id='AK', name='Alaska', capital='Juneau', registration_url='https://www.elections.alaska.gov/Core/voterregistration.php',
           elections_url='https://www.elections.alaska.gov/Core/generalelectioninformation.php')
AZ = State(id='AZ', name='Arizona', capital='Phoenix', registration_url='https://azsos.gov/elections/voting-election/register-vote-or-update-your-current-voter-information',
           elections_url='https://azsos.gov/elections/elections-calendar-upcoming-events')
AR = State(id='AR', name='Arkansas', capital='Little Rock',
           registration_url='https://www.sos.arkansas.gov/elections/for-voters', elections_url='https://www.sos.arkansas.gov/elections')
CA = State(id='CA', name='California', capital='Sacramento',
           registration_url='https://registertovote.ca.gov/', elections_url='https://www.sos.ca.gov/elections')
CO = State(id='CO', name='Colorado', capital='Denver', registration_url='https://www.sos.state.co.us/voter/pages/pub/olvr/verifyNewVoter.xhtml',
           elections_url='https://www.sos.state.co.us/pubs/elections/electionInfo.html')
CT = State(id='CT', name='Connecticut', capital='Hartford', registration_url='https://voterregistration.ct.gov/OLVR/welcome.do',
           elections_url='https://portal.ct.gov/SOTS/Election-Services/Calendars/Election-Calendars')
DE = State(id='DE', name='Delaware', capital='Dover', registration_url='https://ivote.de.gov/VoterView',
           elections_url='https://elections.delaware.gov/calendars.shtml')
DC = State(id='DC', name='District of Columbia', capital='District of Columbia',
           registration_url='https://www.dcboe.org/Voters/Register-To-Vote/Register-to-Vote', elections_url='https://dcboe.org/Community-Outreach/Events')
FL = State(id='FL', name='Florida', capital='Tallahassee', registration_url='https://registertovoteflorida.gov/home',
           elections_url='https://dos.myflorida.com/elections/for-voters/election-dates/')
GA = State(id='GA', name='Georgia', capital='Atlanta', registration_url='https://georgia.gov/register-to-vote',
           elections_url='https://sos.ga.gov/index.php/elections/elections_and_voter_registration_calendars')
HI = State(id='HI', name='Hawaii', capital='Honolulu', registration_url='https://elections.hawaii.gov/register-to-vote/registration/',
           elections_url='https://elections.hawaii.gov/voting/contest-schedule/')
ID = State(id='ID', name='Idaho', capital='Boise', registration_url='https://elections.sos.idaho.gov/ElectionLink/ElectionLink/ApplicationInstructions.aspx',
           elections_url='https://sos.idaho.gov/elections-division/calendars/')
IL = State(id='IL', name='Illinois', capital='Springfield', registration_url='https://ova.elections.il.gov/?Name=Em5DYCKC4wXCKQSXTgsQ9knm%2b5Ip27VC&T=637623864062530637',
           elections_url='https://www.elections.il.gov/Main/CalendarEventsAll.aspx?T=637665305487546022')
IN = State(id='IN', name='Indiana', capital='Indianapolis', registration_url='https://www.in.gov/sos/elections/voter-information/register-to-vote/',
           elections_url='https://www.in.gov/sos/elections/voter-information/')
IA = State(id='IA', name='Iowa', capital='Des Moines', registration_url='https://sos.iowa.gov/elections/voterinformation/voterregistration.html',
           elections_url='https://sos.iowa.gov/elections/electioninfo/3yrelectioncal.html')
KS = State(id='KS', name='Kansas', capital='Topeka', registration_url='https://www.kdor.ks.gov/Apps/VoterReg/Default.aspx',
           elections_url='https://www.sos.ks.gov/elections/elections.html')
KY = State(id='KY', name='Kentucky', capital='Frankfort',
           registration_url='https://fj.usembassy.gov/u-s-citizen-services/voting/', elections_url='')
LA = State(id='LA', name='Louisiana', capital='Baton Rouge', registration_url='https://www.sos.la.gov/ElectionsAndVoting/RegisterToVote/Pages/default.aspx',
           elections_url='https://www.sos.la.gov/ElectionsAndVoting/GetElectionInformation/SearchElectionDates/Pages/default.aspx')
ME = State(id='ME', name='Maine', capital='Augusta', registration_url='https://www.maine.gov/sos/cec/elec/voter-info/votreg.html',
           elections_url='https://www.maine.gov/sos/cec/elec/upcoming/index.html')
MD = State(id='MD', name='Maryland', capital='Annapolis', registration_url='https://elections.maryland.gov/voter_registration/index.html',
           elections_url='https://elections.maryland.gov/elections/')
MA = State(id='MA', name='Massachusetts', capital='Boston', registration_url='https://www.sec.state.ma.us/OVR/',
           elections_url='https://www.sec.state.ma.us/ele/elesched/schedidx.htm')
MI = State(id='MI', name='Michigan', capital='Lansing', registration_url='https://mvic.sos.state.mi.us/Home/RegisterToVote',
           elections_url='https://www.michigan.gov/sos/0,4670,7-127-1633---,00.html')
MN = State(id='MN', name='Minnesota', capital='St. Paul', registration_url='https://www.sos.state.mn.us/elections-voting/register-to-vote/',
           elections_url='https://www.sos.state.mn.us/election-administration-campaigns/elections-calendar/')
MS = State(id='MS', name='Mississippi', capital='Jackson', registration_url='https://www.sos.state.mn.us/elections-voting/register-to-vote/',
           elections_url='https://www.sos.ms.gov/elections-voting')
MO = State(id='MO', name='Missouri', capital='Jefferson City', registration_url='https://www.sos.mo.gov/elections/goVoteMissouri/register',
           elections_url='https://www.sos.mo.gov/elections/calendar/')
MT = State(id='MT', name='Montana', capital='Helena', registration_url='https://sosmt.gov/elections/vote/',
           elections_url='https://sosmt.gov/elections/calendars/')
NE = State(id='NE', name='Nebraska', capital='Lincoln', registration_url='https://www.nebraska.gov/apps-sos-voter-registration/',
           elections_url='https://www.nebraska.gov/featured/elections-voting/')
NV = State(id='NV', name='Nevada', capital='Carson City', registration_url='https://www.nvsos.gov/sos/elections/voters/registering-to-vote',
           elections_url='https://www.nvsos.gov/sos/elections/election-information')
NH = State(id='NH', name='New Hampshire', capital='Concord', registration_url='https://sos.nh.gov/elections/voters/register-to-vote/',
           elections_url='https://www.ncsbe.gov/voting/upcoming-election')
NJ = State(id='NJ', name='New Jersey', capital='Trenton', registration_url='https://nj.gov/state/elections/voter-registration.shtmll',
           elections_url='https://www.state.nj.us/state/elections/election-information.shtml')
NM = State(id='NM', name='New Mexico', capital='Santa Fe', registration_url='https://portal.sos.state.nm.us/OVR/WebPages/InstructionsStep1.aspx',
           elections_url='https://www.sos.state.nm.us/voting-and-elections/upcoming-elections/')
NY = State(id='NY', name='New York', capital='Albany', registration_url='https://www.elections.ny.gov/VotingRegister.html',
           elections_url='https://vote.nyc/page/upcoming-elections')
NC = State(id='NC', name='North Carolina', capital='Raleigh', registration_url='https://www.ncsbe.gov/registering',
           elections_url='https://www.ncsbe.gov/voting/upcoming-election')
ND = State(id='ND', name='North Dakota', capital='Bismarck', registration_url='https://vote.nd.gov/PortalListDetails.aspx?ptlhPKID=73&ptlPKID=5',
           elections_url='https://vip.sos.nd.gov/pdfs/Portals/electioncalendar.pdf')
OH = State(id='OH', name='Ohio', capital='Columbus', registration_url='https://olvr.ohiosos.gov/',
           elections_url='https://www.ohiosos.gov/elections/voters/current-voting-schedule/')
OK = State(id='OK', name='Oklahoma', capital='Oklahoma City', registration_url='https://oklahoma.gov/elections/voter-info/register-to-vote.html',
           elections_url='https://hosting.okelections.us/electionlist.html')
OR = State(id='OR', name='Oregon', capital='Salem', registration_url='https://sos.oregon.gov/voting/Pages/registration.aspx?lang=en',
           elections_url='https://sos.oregon.gov/voting/Pages/current-election.aspx')
PA = State(id='PA', name='Pennsylvania', capital='Harrisburg', registration_url='https://www.pavoterservices.pa.gov/Pages/VoterRegistrationApplication.aspx',
           elections_url='https://www.votespa.com/About-Elections/Pages/Upcoming-Elections.aspx')
RI = State(id='RI', name='Rhode Island', capital='Providence', registration_url='https://vote.sos.ri.gov/Home/RegistertoVote?ActiveFlag=1',
           elections_url='https://elections.ri.gov/elections/upcoming/index.php')
SC = State(id='SC', name='South Carolina', capital='Columbia', registration_url='https://www.scvotes.gov/south-carolina-voter-registration-information',
           elections_url='https://www.scvotes.gov/schedule-elections')
SD = State(id='SD', name='South Dakota', capital='Pierre', registration_url='https://sdsos.gov/elections-voting/voting/register-to-vote/default.aspx',
           elections_url='https://sdsos.gov/elections-voting/upcoming-elections/general-information/default.aspx')
TN = State(id='TN', name='Tennessee', capital='Nashville', registration_url='https://sos.tn.gov/products/elections/register-vote',
           elections_url='https://sos.tn.gov/elections/election-information')
TX = State(id='TX', name='Texas', capital='Austin', registration_url='https://www.votetexas.gov/register/index.html',
           elections_url='https://www.sos.state.tx.us/elections/voter/important-election-dates.shtml')
UT = State(id='UT', name='Utah', capital='Salt Lake City', registration_url='https://voteinfo.utah.gov/learn-about-registering-to-vote/',
           elections_url='https://voteinfo.utah.gov/election-dates-deadlines/')
VT = State(id='VT', name='Vermont', capital='Montpelier', registration_url='https://sos.vermont.gov/elections/voters/registration/',
           elections_url='https://sos.vermont.gov/elections-calendar/')
VA = State(id='VA', name='Virginia', capital='Richmond', registration_url='https://www.elections.virginia.gov/registration/',
           elections_url='https://www.elections.virginia.gov/casting-a-ballot/calendars-schedules/upcoming-elections.html')
WA = State(id='WA', name='Washington', capital='Olympia', registration_url='https://voter.votewa.gov/WhereToVote.aspx',
           elections_url='https://www.elections.virginia.gov/casting-a-ballot/calendars-schedules/upcoming-elections.html')
WV = State(id='WV', name='West Virginia', capital='Charleston', registration_url='https://ovr.sos.wv.gov/Register/Landing',
           elections_url='https://sos.wv.gov/elections/Pages/default.aspx')
WI = State(id='WI', name='Wisconsin', capital='Madison', registration_url='https://myvote.wi.gov/en-us/Register-To-Vote',
           elections_url='https://elections.wi.gov/elections-voting/elections')
WY = State(id='WY', name='Wyoming', capital='Cheyenne', registration_url='https://sos.wyo.gov/Elections/State/RegisteringToVote.aspx',
           elections_url='https://sos.wyo.gov/Elections/Default.aspx')

db.session.add_all([AK, AL, AR, AZ, CA, CO, CT, DE, DC, FL, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI,
                   MN, MS, MO, MT, NE, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY])
db.session.commit()
