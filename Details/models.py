from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Skills(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.TextField()
    pastexp = models.TextField()
    workexpec = models.TextField()
    bio = models.TextField()
    rating = models.IntegerField(default=0)

class SkillSet(models.Model):
    skills = models.ForeignKey(
        Skills,
        on_delete= models.CASCADE,
        related_name= 'skillset'
    )
    description = models.CharField(max_length=50)
    
class TeamsManager(models.Manager):
    def addMember(self,team,user):
        team.members.create(team=team, user=user)
        team.save()

    def removeMember(self,team,user):
        team.members.filter(team=team, user=user)[0].delete()
        if len(team.members.all()) == 0:
            team.delete()
class Teams(models.Model):
    teamname = models.CharField(max_length = 50)
    def __str__(self):
        return self.teamname
    objects = TeamsManager()

class TeamMembers(models.Model):
    team = models.ForeignKey(
        Teams,
        on_delete= models.CASCADE,
        related_name= "members"
    )
    user = models.ForeignKey(
        User,
        on_delete= models.CASCADE,
        related_name= "users"
    )

class TeamDesc(models.Model):
    team = models.OneToOneField(
        Teams,
        on_delete= models.CASCADE
    )
    teamdescription = models.TextField()
    teammotive = models.TextField()
    
class UserRequests(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uruser'
    )
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        related_name='urteam'
    )

class TeamRequests(models.Model):
    team = models.ForeignKey(
        Teams,
        on_delete=models.CASCADE,
        related_name='trteam'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='truser'
    )