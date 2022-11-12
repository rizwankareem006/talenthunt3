from django.contrib.auth.models import User
from .models import TeamMembers, UserRequests, TeamRequests, Teams
class CardDetails:
    def __init__(self, user, sks, skset):
        self.username = user.username
        self.fullname = user.get_full_name()
        self.skillset = list(skset)
        self.workexpec = sks.workexpec
        self.rating = sks.rating
    
class PageNumber:
    def __init__(self, currentPage):
        self.current_page = currentPage
    
    @property
    def nextPage(self):
        return self.current_page+1
    
    @property
    def previousPage(self):
        return self.current_page-1

class ProfileDetails:
    def __init__(self,user):
        self.username = user.username
        self.firstname = user.first_name
        self.lastname = user.last_name
        self.email = user.email
        self.mobile = user.extuser.mobile
        self.gender = user.extuser.gender
        self.dob = str(user.extuser.dob)
        self.skillset = list(user.skills.skillset.all())
        self.specialization = user.skills.specialization
        self.pastexp = user.skills.pastexp
        self.workexpec = user.skills.workexpec
        self.bio = user.skills.bio
        self.rating = user.skills.rating
    
class TeamProfile:
    def __init__(self, team):
        self.primary_key = team.pk
        self.teamname = team.teamname
        self.teamdescription = team.teamdesc.teamdescription
        self.teammotive = team.teamdesc.teammotive
        self.teammembers = list(team.members.all())
        
class ProfileTeamList:
    def __init__(self, teams):
        self.primary_keys = []
        self.teamname = []
        for item in teams:
            self.primary_keys.append(item.team.pk)
            self.teamname.append(item.team.teamname)
        
class TeamProfileList:
    def __init__(self,users,requser):
        self.usernames = []
        self.fullnames = []
        for item in users:
            if item.user.username != requser:
                self.usernames.append(item.user.username)
                self.fullnames.append(item.user.get_full_name())

class ProfileReqs:
    def __init__(self,user):
        self.requests = []
        self.primary_keys = []
        teams = user.uruser.all()
        for item in teams:
            self.requests.append(item.team.teamname)
            self.primary_keys.append(item.team.pk)

class TeamReqs:
    def __init__(self,team):
        self.requests = []
        self.usernames = []
        users = team.trteam.all()
        for item in users:
            self.requests.append(item.user.get_full_name())
            self.usernames.append(item.user.username)

class ProfileSendRequest:
    def __init__(self,sendername,receivername):
        sender = User.objects.get(username=sendername)
        receiver = User.objects.get(username=receivername)
        teamlist = set()
        st = TeamMembers.objects.filter(user=sender)
        for item in st:
            teamlist.add(item.team.pk)
        rt = TeamMembers.objects.filter(user=receiver)
        for item in rt:
            teamlist.discard(item.team.pk)
        rr = UserRequests.objects.filter()
        for item in rr:
            teamlist.discard(item.team.pk)
        self.primary_keys = list(teamlist)
        self.teamnames = []
        for item in self.primary_keys:
            self.teamnames.append(Teams.objects.get(pk=item).teamname)


        
