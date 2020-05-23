from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.template import loader
from .commands import *
from .forms import *
import ctypes  # An included library with Python install.

# Create your views here.

worker = CommandWorker()
cmds = Commands()


class Home(View):
    def get(self, req):
        template = loader.get_template('index.html')
        context = {}

        if 'current_role' in req.session:
            context['cmds'] = cmds.getCmds(req.session['current_role'])

        else:
            context['cmds'] = []

        return HttpResponse(template.render(context, req))

    def post(self, req):
        template = loader.get_template('index.html')
        context = {}
        if 'current_role' in req.session:
            context['cmds'] = cmds.getCmds(req.session['current_role'])
            context['text'] = "Welcome to the TA Management App."

        return HttpResponse(template.render(context, req))


class CreateCourse(View):
    def get(self, req):
        template = loader.get_template('form.html')
        context = {}
        context['form'] = CreateCourseForm()
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CreateCourseForm(req.POST)
        template = loader.get_template('table.html')
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'create course "{form.cleaned_data["name"]}" '
                                               f'"{form.cleaned_data["section"]}" ')
            context['form'] = CreateCourseForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['courses'] = ch.executeCommand(f'list courses')
        return HttpResponse(template.render(context, req))


class ViewLabs(View):
    def get(self, req):
        template = loader.get_template('labTable.html')
        context = {}
        lcourse = req.GET.get('labCourse', '')
        ch = CommandWorker(req.session['current_user'])
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['labs'] = ch.executeCommand(f'view labs ' + lcourse)
        context['labCourse'] = lcourse
        return HttpResponse(template.render(context, req))


class CreateLab(View):
    def get(self, req):
        template = loader.get_template('form.html')
        context = {}
        context['form'] = CreateLabForm()
        context['c'] = cmds.getCmds(req.session['current_role'])
        context['labCourse'] = req.GET.get('labCourse', '')
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CreateLabForm(req.POST)
        template = loader.get_template('labTable.html')
        context = {}
        lcourse = req.GET.get('labCourse', '')
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'create lab ' + lcourse + " " +
                                               f'"{form.cleaned_data["section"]}" ')
            context['form'] = CreateLabForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['labs'] = ch.executeCommand(f'view labs ' + lcourse)
        context['labCourse'] = lcourse
        return HttpResponse(template.render(context, req))


class EditLab(View):

    def get(self, req):
        template = loader.get_template('editLab.html')
        context = {}
        lcourse = req.GET.get('labCourse', '')
        lsec = req.GET.get('labSection', '')
        c = Course.objects.get(name=lcourse)
        l = Lab.objects.get(course=c, section=lsec)
        form = EditLabForm()
        form.initial['section'] = l.section
        form.initial['location'] = l.location
        form.initial['startTime'] = l.startTime
        form.initial['endTime'] = l.endTime
        form.initial['dates'] = l.dates
        context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        ch = CommandWorker(req.session['current_user'])
        context['labs'] = ch.executeCommand(f'view labs ' + lcourse)
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = EditLabForm(req.POST)
        template = loader.get_template('labTable.html')
        context = {}
        lcourse = req.GET.get('labCourse', '')
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'edit lab ' + lcourse + " " +
                                               f'"{form.cleaned_data["section"]}" '
                                               f'"{form.cleaned_data["location"]}" '
                                               f'"{form.cleaned_data["startTime"]}" '
                                               f'"{form.cleaned_data["endTime"]}" '
                                               f'"{form.cleaned_data["dates"]}" ')
            context['form'] = EditLabForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        ch = CommandWorker(req.session['current_user'])
        context['labs'] = ch.executeCommand(f'view labs ' + lcourse)
        return HttpResponse(template.render(context, req))


class EditCourse(View):

    def get(self, req):
        template = loader.get_template('editCourse.html')
        context = {}
        cname = req.GET.get('courseName', '')
        csec = req.GET.get('courseSection', '')
        c = Course.objects.get(name=cname, section=csec)

        form = EditCourseForm()
        form.initial['name'] = c.name
        form.initial['section'] = c.section
        form.initial['dates'] = c.dates
        form.initial['location'] = c.location
        form.initial['startTime'] = c.startTime
        form.initial['endTime'] = c.endTime

        context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        ch = CommandWorker(req.session['current_user'])
        context['courses'] = ch.executeCommand(f'list courses')
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = EditCourseForm(req.POST)
        template = loader.get_template('table.html')
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'edit course "{form.cleaned_data["name"]}" '
                                               f'"{form.cleaned_data["section"]}" '
                                               f'"{form.cleaned_data["location"]}" '
                                               f'"{form.cleaned_data["startTime"]}" '
                                               f'"{form.cleaned_data["endTime"]}" '
                                               f'"{form.cleaned_data["dates"]}" ')

            context['form'] = EditCourseForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        ch = CommandWorker(req.session['current_user'])
        context['courses'] = ch.executeCommand(f'list courses')
        return HttpResponse(template.render(context, req))


'''class EditProfile(View):

    def get(self, req):
        template = loader.get_template('form.html')
        context = {}
        context['form'] = EditProfileForm()
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        template = loader.get_template('profile.html')
        form = EditProfileForm(req.POST)

        
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'edit profile "{form.cleaned_data["resume"]}" '
                                               f'"{form.cleaned_data["schedule"]}" '
                                               f'"{form.cleaned_data["preferences"]}" ')

            context['form'] = EditProfileForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['user'] = ch.executeCommand(f'view profile')
        return HttpResponse(template.render(context, req))'''


class ListCourses(View):
    def get(self, req):
        template = loader.get_template('table.html')
        context = {}
        ch = CommandWorker(req.session['current_user'])
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['courses'] = ch.executeCommand(f'list courses')
        return HttpResponse(template.render(context, req))


class DeleteCourse(View):
    def get(self, req):
        template = loader.get_template('table.html')
        context = {}

        cname = req.GET.get('courseName','')
        print(cname)
   
        # this is alternative way to ask for validation
        '''if ctypes.windll.user32.MessageBoxW(0, "Do You Want to Delete the Course", "Course Deletion", 1) ==1:
            c = Course.objects.get(name=cname).delete()
            context['out'] = 'Course Deleted'
        else: 
            context['out'] = 'Course was not Deleted'''
        c = Course.objects.get(name=cname).delete()
        context['out'] = 'Course Deleted'
        ch = CommandWorker(req.session['current_user'])
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['courses'] = ch.executeCommand(f'list courses')
        return HttpResponse(template.render(context, req))


class DeleteUser(View):
    def get(self, req):
        template = loader.get_template('userTable.html')
        context = {}
        cname = req.GET.get('email', '')
        # this is alternative way to ask for validation
        '''if ctypes.windll.user32.MessageBoxW(0, "Do You Want to Delete the User", "User Deletion", 1) ==1:
            c = User.objects.get(email=cname).delete()
            context['out'] = 'User Deleted'
        else: 
            context['out'] = 'User was not Deleted'''
        c = User.objects.get(email=cname).delete()
        context['out'] = 'User Deleted'
        ch = CommandWorker(req.session['current_user'])
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['users'] = ch.executeCommand(f'list users')
        return HttpResponse(template.render(context, req))


class ListUsers(View):

    def get(self, req):
        template = loader.get_template('userTable.html')
        context = {}
        ch = CommandWorker(req.session['current_user'])
        context['users'] = ch.executeCommand(f'list users')
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        return HttpResponse(template.render(context, req))


class CreateUser(View):

    def get(self, req):
        template = loader.get_template('form.html')
        context = {}
        context['form'] = CreateUserForm()
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = CreateUserForm(req.POST)
        template = loader.get_template('userTable.html')
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'create user "{form.cleaned_data["email"]}" '
                                               f'"{form.cleaned_data["password"]}" '
                                               f'"{form.cleaned_data["role"]}" ')
            context['form'] = CreateUserForm()
        else:
            context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['users'] = ch.executeCommand(f'list users')

        return HttpResponse(template.render(context, req))


class EditUser(View):

    def get(self, req):
        template = loader.get_template('editUser.html')
        context = {}
        eml = req.GET.get('email', '')
        u = User.objects.get(email=eml)
        form = EditUserForm()
        form.initial['email'] = u.email
        form.initial['firstName'] = u.firstName
        form.initial['lastName'] = u.lastName
        form.initial['role'] = u.role
        form.initial['phone'] = u.phone
        form.initial['address'] = u.address
        form.initial['officeLocation'] = u.officeLocation
        form.initial['officeHours'] = u.officeHours
        form.initial['officeHoursDates'] = u.officeHoursDates
        form.initial['resume'] = u.resume
        form.initial['schedule'] = u.schedule
        form.initial['Preferences'] = u.preferences
        context['form'] = form
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        ch = CommandWorker(req.session['current_user'])
        context['users'] = ch.executeCommand(f'list users')
        return HttpResponse(template.render(context, req))

    def post(self, req):
        form = EditUserForm(req.POST)
        template = loader.get_template('userTable.html')
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            context['out'] = ch.executeCommand(f'edit user "{form.cleaned_data["email"]}" '
                                               f'"{form.cleaned_data["firstName"]}" '
                                               f'"{form.cleaned_data["lastName"]}" '
                                               f'"{form.cleaned_data["role"]}" '
                                               f'"{form.cleaned_data["phone"]}" '
                                               f'"{form.cleaned_data["address"]}" '
                                               f'"{form.cleaned_data["officeHours"]}" '
                                               f'"{form.cleaned_data["officeHoursDates"]}" '
                                               f'"{form.cleaned_data["officeLocation"]}" '
                                               f'"{form.cleaned_data["resume"]}" '
                                               f'"{form.cleaned_data["schedule"]}" '
                                               f'"{form.cleaned_data["preferences"]}" '

                                               )
            context['form'] = EditUserForm()
        else:
            context['form'] = form
        
        ch = CommandWorker(req.session['current_user'])
       # context['user'] = ch.executeCommand(f'view profile')
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['users'] = ch.executeCommand(f'list users')
        return HttpResponse(template.render(context, req))


class ViewProfile(View):
    def get(self, req):
        template = loader.get_template('profile.html')
        context = {}
        ch = CommandWorker(req.session['current_user'])
        context['user'] = ch.executeCommand(f'view profile')
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        return HttpResponse(template.render(context, req))


class ViewUser(View):

    def get(self, req):
        template = loader.get_template('profile.html')
        context = {}
        eml = req.GET.get('email', '')
        c = User.objects.get(email=eml)
        ch = CommandWorker(req.session['current_user'])
        context['user'] = ch.executeCommand(f'view user')
        #context['user'] = ch.view_user(eml)
        context['cmds'] = cmds.getCmds(req.session['current_role'])

        return HttpResponse(template.render(context, req))


class Login(View):

    def get(self, req):
        template = loader.get_template('form.html')
        context = {}
        context['form'] = LoginForm()

        if 'current_role' in req.session:
            context['cmds'] = cmds.getCmds(req.session['current_role'])
        else:
            context['cmds'] = []
        return HttpResponse(template.render(context, req))

    def post(self, req):
        context = {}
        form = LoginForm(req.POST)
        if form.is_valid():
            while True:
                out = worker.executeCommand(f'login {form.cleaned_data["email"]} "{form.cleaned_data["password"]}"')
                if out.startswith('Logged in as'):
                    break
                else:
                    out = 'Email and/or password is wrong. Try again'

            if out.startswith('Logged in as'):
                template = loader.get_template('index.html')
                context['out'] = out
                req.session['current_user'] = form.cleaned_data['email']
                u = User.objects.filter(email=form.cleaned_data['email']).first()
                req.session['current_role'] = u.role
            if 'current_role' in req.session:
                context['cmds'] = cmds.getCmds(req.session['current_role'])
            else:
                context['cmds'] = []

            return HttpResponse(template.render(context, req))


class Logout(View):
    def get(self, req):
        template = loader.get_template('index.html')
        context = {}
        req.session['current_user'] = None
        req.session['current_role'] = None
        context['form'] = None
        context['cmds'] = []

        return HttpResponse(template.render(context, req))

    def post(self, req):
        template = loader.get_template('index.html')
        if req.session['current_user']:
            out = 'Successfully logged out'
        else:
            out = 'You must be logged in to log out'
        context = {}
        context['out'] = out
        req.session['current_user'] = None
        req.session['current_role'] = None
        context['cmds'] = cmds.addCmd(req.session['current_role'])
        return HttpResponse(template.render(context, req))


class AssignTa(View):

    def get(self, req):
        template = loader.get_template('getAssignTa.html')
        #courseNames = AssignTaForm.cleaned_data["courses"].values_list('name', flat=True)
        #taEmails = AssignTaForm.cleaned_data["tas"].values_list('email', flat=True)
        context = {'form': AssignTaForm(), 'cmds': cmds.getCmds(req.session['current_role'])}
        return HttpResponse(template.render(context, req))

    def post(self, req):
        template = loader.get_template('postAssignTa.html')
        form = AssignTaForm(req.POST)
        context = {}
        if form.is_valid():
            ch = CommandWorker(req.session['current_user'])
            tas = form.cleaned_data["tas"]
            course = form.cleaned_data["course"]

            ch.assign_ta(course=course, tas=tas)

            tasEmailList = tas.values_list('email', flat=True)

            context['course'] = course
            context['tas'] = tasEmailList
            

        return HttpResponse(template.render(context, req))


class Validate(View):
    def get(self, req):
        template = loader.get_template('table.html')
        context = {}
        ch = CommandWorker(req.session['current_user'])
        context['cmds'] = cmds.getCmds(req.session['current_role'])
        context['courses'] = ch.executeCommand(f'list courses ')
        context['out'] = ch.executeCommand(f'validate')
        return HttpResponse(template.render(context, req))
