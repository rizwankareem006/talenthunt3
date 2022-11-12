from django.shortcuts import render,redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from Details.iterator import UserIterator, TeamIterator
from .models import Skills, SkillSet, Teams, TeamDesc, TeamMembers, UserRequests, TeamRequests
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponseNotFound
from .datastructure import CardDetails, PageNumber, ProfileDetails, TeamProfile, ProfileTeamList, TeamProfileList, ProfileReqs, TeamReqs, ProfileSendRequest
from django.db.models import Q

# Create your views here.
def signout(request):
    users = User.objects.all()
    teams = Teams.objects.all()

    user_iterator = UserIterator(users)
    team_iterator = TeamIterator(teams)

    for i in user_iterator:
        print(i)

    for i in team_iterator:
        print(i)
        
    logout(request)
    return redirect('Registration:Login')

@login_required
def skills(request):
    if request.method == "POST":
        skill_list = request.POST.getlist('skillset[]')
        valid = True
        if valid:
            skills = Skills(user = request.user, specialization = request.POST['specialization'], pastexp = request.POST['pastexp'], workexpec = request.POST['workexpec'], bio = request.POST['bio'])
            skills.save()
            for i in skill_list:
                obj = skills.skillset.create(description = i)
                obj.save()
            response = {
            'status':0,
            'message':'OK',
            }
            return JsonResponse(response)
    return render(request,'Details/skills.html')

@login_required
def feed(request,page=1):
    if request.method == "GET":
        skilldetails = Skills.objects.all().order_by("-rating")
        start = 10*(page-1)
        end = start + 10
        carddet = []
        for i in range(start, min(len(skilldetails),end)):
            sks = skilldetails[i]
            uobj = User.objects.get(username = sks.user)
            if uobj.username != str(request.user):
                skset = list(sks.skillset.all())
                cd = CardDetails(uobj,sks,skset)
                carddet.append(cd)
        nop = len(skilldetails)//10
        page_number = PageNumber(page)
        context = {'page_number':page_number, 'carddet':carddet, 'np':nop}
        return render(request,'Details/feed.html',context = context)

@login_required
def profile(request,username):
    if str(request.user) == username:
        user = User.objects.get(username = request.user)
        pd = ProfileDetails(user)
        teams = TeamMembers.objects.filter(user=user)
        td = ProfileTeamList(teams)
        reqs = ProfileReqs(user)
        context = {'pd':pd,'td':td,'reqs':reqs,'owner':True}
    else:
        user = User.objects.get(username = username)
        pd = ProfileDetails(user)
        teams = TeamMembers.objects.filter(user=user)
        td = ProfileTeamList(teams)
        reqs = ProfileSendRequest(str(request.user),username)
        context = {'pd':pd, 'td':td,'reqs':reqs,'owner':False}
    return render(request,'Details/profile.html', context=context)

@login_required
def profileupdate(request, username):
    if request.method == "POST":
        user = User.objects.get(username = request.user)
        user.first_name = request.POST['firstname']
        user.last_name = request.POST['lastname']
        user.email = request.POST['email']
        user.extuser.gender = request.POST['gender']
        user.extuser.mobile = request.POST['mobile']
        user.extuser.dob = request.POST['dob']
        li = request.POST.getlist('skillset[]')
        skills = Skills.objects.get(user=user)
        skills.skillset.all().delete()
        for i in li:
            item = SkillSet.objects.create(skills = skills, description=i)
            item.save()
        user.skills.specialization = request.POST['specialization']
        user.skills.pastexp = request.POST['pastexp']
        user.skills.workexpec = request.POST['workexpec']
        user.skills.bio = request.POST['bio']
        user.skills.save()
        user.extuser.save()
        user.save()
        response = {
            'status':0,
            'message':"Profile Updated Successfully!"
        }
        return JsonResponse(response)

@login_required
def createteam(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        teamname = str(request.POST['teamname']).strip()
        teamdescription = str(request.POST['teamdescription']).strip()
        teammotive = str(request.POST['teammotive']).strip()
        if teamname == "":
            error = "Team name cannot be empty!"
            context = {'error':error}
        elif teamdescription == "":
            error = "Team description cannot be empty!"
            context = {'error':error}
        elif teammotive == "":
            error = "Team motive cannot be empty!"
            context = {'error':error}
        else:
            team = Teams.objects.create(teamname = teamname)
            teamdesc = TeamDesc.objects.create(team=team, teamdescription=teamdescription, teammotive=teammotive)
            Teams.objects.addMember(team,user)
            teamdesc.save()
            team.save()
            return redirect('Details:TeamProfile', team=team.pk)
    else:
        context = {}
    return render(request, 'Details/teamcreation.html', context=context)

@login_required
def teamprofile(request, team):
    user = User.objects.get(username = request.user)
    teamitem = Teams.objects.filter(pk=team)
    context={}
    if not teamitem.exists():
        return HttpResponseNotFound('<h3>Page not found</h3>')
    else:
        if request.method == "POST":
            teamdescription = str(request.POST['teamdescription']).strip()
            teammotive = str(request.POST['teammotive']).strip()
            if teamdescription == "":
                error = "Team description cannot be empty!"
                context.update({'message':error})
            elif teammotive == "":
                error = "Team motive cannot be empty!"
                context.update({'message':error})
            else:
                ti = teamitem[0]
                ti.teamdesc.teamdescription = teamdescription
                ti.teamdesc.teammotive = teammotive
                ti.teamdesc.save()
                ti.save()
                context['message']="Updated Successfully!"
        owner = teamitem[0].members.filter(user = user).exists()
        tp = TeamProfile(teamitem[0])
        userlist = TeamMembers.objects.filter(team=teamitem[0])
        mems = TeamProfileList(userlist,str(request.user))
        reqs = TeamReqs(teamitem[0])
        reqsent = TeamRequests.objects.filter(team=teamitem[0], user=user).exists()
        context.update({'tp':tp,'pd':mems,'reqs':reqs,'owner':owner,'reqsent':reqsent})
        return render(request, 'Details/teamprofile.html', context = context)

@login_required
def teamacceptrequest(request,team,user):
    if request.method == "POST":
        t = Teams.objects.get(pk=team)
        u = User.objects.get(username=user)
        tr = TeamRequests.objects.get(team=t, user=u)
        tr.delete()
        Teams.objects.addMember(t,u)
        return redirect('Details:TeamProfile', team=t.pk)

@login_required
def teamdeclinerequest(request,team,user):
    if request.method == "POST":
        t = Teams.objects.get(pk=team)
        u = User.objects.get(username=user)
        tr = TeamRequests.objects.get(team=t, user=u)
        tr.delete()
        return redirect('Details:TeamProfile', team=t.pk)

@login_required
def useracceptrequest(request,user,team):
    if request.method == "POST":
        t = Teams.objects.get(pk=team)
        u = User.objects.get(username=user)
        ur = UserRequests.objects.get(user=u, team=t)
        ur.delete()
        Teams.objects.addMember(t,u)
        return redirect('Details:Profile', username=u.username)

@login_required
def userdeclinerequest(request,user,team):
    if request.method == "POST":
        t = Teams.objects.get(pk=team)
        u = User.objects.get(username=user)
        ur = UserRequests.objects.get(user=u, team=t)
        ur.delete()
        return redirect('Details:Profile', username=u.username)

@login_required
def usersendrequest(request,team,user):
    if request.method == "POST":
        t = Teams.objects.get(pk=team)
        u = User.objects.get(username=user)
        ur = UserRequests.objects.create(user=u, team=t)
        ur.save()
        return redirect('Details:Profile', username=u.username)

@login_required
def teamsendrequest(request,team):
    if request.method == "POST":
        u = User.objects.get(username=str(request.user))
        t = Teams.objects.get(pk=team)
        tr = TeamRequests.objects.create(team=t, user=u)
        tr.save()
        return redirect('Details:TeamProfile', team=t.pk)

@login_required
def teammembersuccess(request,team,user):
    if request.method == "POST":
        u = User.objects.get(username=user)
        t = Teams.objects.get(pk=team)
        Teams.objects.removeMember(t,u)
        u.skills.rating += 10
        u.skills.save()
        return redirect('Details:TeamProfile', team=t.pk)

@login_required
def teammemberfailure(request,team,user):
    if request.method == "POST":
        u = User.objects.get(username=user)
        t = Teams.objects.get(pk=team)
        Teams.objects.removeMember(t,u)
        u.skills.rating -= 10
        return redirect('Details:TeamProfile', team=t.pk)

@login_required
def resign(request,team,user):
    if request.method == "POST":
        u = User.objects.get(username=user)
        t = Teams.objects.get(pk=team)
        Teams.objects.removeMember(t,u)
        return redirect('Details:Profile', username=u.username)

@login_required
def search(request,page=1):
        print(request.GET)
        users = User.objects.filter(Q(first_name__icontains=request.GET["search"])|Q(last_name__icontains=request.GET["search"]))
        start = 10*(page-1)
        end = start + 10
        carddet = []
        for i in range(start, min(len(users),end)):
            uobj = users[i]
            sks = Skills.objects.get(user = uobj)
            if uobj.username != str(request.user):
                skset = list(sks.skillset.all())
                cd = CardDetails(uobj,sks,skset)
                carddet.append(cd)
        nop = len(users)//10
        page_number = PageNumber(page)
        context = {'page_number':page_number, 'carddet':carddet, 'np':nop}
        return render(request,'Details/feed.html',context = context)