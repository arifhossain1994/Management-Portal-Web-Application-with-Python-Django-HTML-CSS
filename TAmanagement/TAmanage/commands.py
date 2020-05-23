from .models import *
import shlex


class Commands:
    def __init__(self):
        self.cmdList = []
        self.addCmd(Role.Administrator, "Create Course", "/createCourse")
        self.addCmd(Role.Administrator, "Create User", "/createUser")
        self.addCmd(Role.Administrator, "Assign Instructors/TAs", "/assignTas")
        self.addCmd([Role.Administrator, Role.Instructor, Role.TA], "View/Edit Profile", "/viewProfile")
        # self.addCmd([Role.Administrator, Role.Instructor, Role.TA], "Edit Profile", "/editProfile")
        self.addCmd([Role.Administrator, Role.Instructor, Role.TA], "List Courses/Validate", "/listCourses")
        self.addCmd([Role.Administrator, Role.Instructor, Role.TA], "List Users", "/listUsers")

    def addCmd(self, cmdrole: Role, cmdtxt, cmdurl):
        if isinstance(cmdrole, list):
            for i in cmdrole:
                cmd = {"cmdRole": i, "cmdTxt": cmdtxt, "cmdUrl": cmdurl}
                self.cmdList.append(cmd)
        else:
            cmd = {"cmdRole": cmdrole, "cmdTxt": cmdtxt, "cmdUrl": cmdurl}
            self.cmdList.append(cmd)

    def getCmds(self, forrole: Role):
        cmdList = []
        for i in self.cmdList:
            if i["cmdRole"] == forrole:
                cmdList.append(i)
        return cmdList


class CommandWorker:
    def __init__(self, currentUserEmail=None):
        u = User.objects.filter(email=currentUserEmail).first()
        self.currentUser = u

    def executeCommand(self, cmdstring: str) -> str:
        try:
            cmd = shlex.split(cmdstring)
        except:
            return 'Badly formatted command'

        worker = {
            'create': {
                'course': self.create_course,
                'user': self.create_user,
                'lab': self.create_lab,
            },
            'edit': {
                'course': self.edit_course,
                'user': self.edit_user,
                'profile': self.edit_profile,
                'lab': self.edit_lab,
            },
            'list': {
                'courses': self.list_courses,
                'users': self.list_users,
            },
            'view': {
                'profile': self.view_profile,
                'user': self.view_user,
                'labs': self.view_labs,
            },
            'delete': {
                'user': self.delete_user,
                'course': self.delete_course,
            },
            'login': self.login,
            'logout': self.logout,
            'assignTa': self.assign_ta,
            'validate': self.validate,
        }
        while type(worker) is dict:
            try:
                worker = worker[cmd[0].lower()]
            except Exception as e:
                return 'Not a valid command'
            cmd.pop(0)
        try:
            return worker(cmd)
        except Exception as e:
            return 'error - %s' % e

    def create_course(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can create a course'
        if len(cmd) != 2:
            return 'Invalid number of parameters'
        c = Course.objects.filter(name=cmd[0], section=cmd[1])
        if c:
            return 'Course Already Exists'
        c = Course(name=cmd[0], section=cmd[1])
        c.save()
        return 'Course Added'

    def view_labs(self, cmd: [str]):
        if not self.currentUser:
            return 'Need to be logged in to list courses'
        cs = Course.objects.get(name=cmd[0])
        labs = Lab.objects.filter(course=cs)
        return labs

    def create_lab(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can create a lab'
        if len(cmd) < 2:
            return 'Invalid number of parameters'
        if len(cmd) > 2:
            return 'Invalid number of parameters'
        cs = Course.objects.get(name=cmd[0])
        c = Lab.objects.filter(course=cs, section=cmd[1])
        if c:
            return 'Lab Already Exists'
        section = cmd[1]
        c = Lab(course=cs, section=section)
        c.save()
        return "Lab Added"

    def edit_lab(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can edit a lab'
        if len(cmd) < 6:
            return 'Invalid number of parameters'
        if len(cmd) > 6:
            return 'Invalid number of parameters'
        c = Course.objects.get(name=cmd[0])
        l = Lab.objects.get(course=c, section=cmd[1])
        valid_dates = {"M", "T", "W", "R", "F", "S", "Online"}
        if l:
            l.section = cmd[1]
            l.location = cmd[2]
            l.startTime = cmd[3]
            l.endTime = cmd[4]
            l.save()
            for ch in cmd[5]:
                if valid_dates.intersection(ch):
                    continue
                else:
                    return 'Invalid date(s)'
            l.dates = cmd[5]
        else:
            return 'Lab does not yet exist'
        l.save()
        return 'Lab Updated'

    def list_courses(self, cmd: [str]):
        if not self.currentUser:
            return 'Need to be logged in to list courses'
        if len(cmd) != 0:
            return 'Invalid number of parameters'
        courses = Course.objects.all()
        return courses

    def list_users(self, cmd: [str]):
        if not self.currentUser:
            return 'Only a current user can list users'
        if len(cmd) != 0:
            return 'Invalid number of parameters'
        users = User.objects.all()
        return users

    def delete_user(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return "Only Admin Can Delete User"
        v = User.objects.get(self)
        if v == self.currentUser:
            return "Cannot Delete Yourself"
        v.delete()
        return "User Deleted"

    def delete_course(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return "Only Admin Can Delete Course"
        v = Course.objects.get(self)
        v.delete()
        return "Course Deleted"

    def view_profile(self, cmd: [str]):
        if not self.currentUser:
            return 'Only a current user can view profile'
        if len(cmd) != 0:
            "Invalid number of parameters"
        user = User.objects.get(email=self.currentUser.email)
        return user

    def view_user(self, cmd: [str]):
        if not self.currentUser.has_role(Role.Administrator):
            return 'Only a current user can view user'
        if len(cmd) < 1:
            "Invalid number of parameters"
        user = User.objects.get(email=cmd[0])
        return user

    def edit_course(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can edit a course'
        if len(cmd) < 1:
            return 'Invalid number of parameters'
        if len(cmd) > 6:
            return 'Invalid number of parameters'
        c = Course.objects.get(name=cmd[0])
        valid_dates = {"M", "T", "W", "R", "F", "S", "Online"}
        if c:
            c.section = cmd[1]
            c.location = cmd[2]
            c.startTime = cmd[3]
            c.endTime = cmd[4]
            c.save()
            for ch in cmd[5]:
                if valid_dates.intersection(ch):
                    continue
                else:
                    return 'Invalid date(s)'
            c.dates = cmd[5]
        else:
            return 'Course does not yet exist'
        c.save()
        return 'Course Updated'

    def assign_ta(self, course, tas):
        if not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can assign TAs'

        tas_list = list(tas)
        for x in tas_list:
            course.graderTAs.add(x)

        return course

    def edit_user(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can edit a user'
        if len(cmd) < 1:
            return 'Invalid number of parameters'
        valid_dates = {"M", "T", "W", "R", "F", "S"}
        u = User.objects.get(email=cmd[0])
        if u:
            u.firstName = cmd[1]
            u.lastName = cmd[2]
            u.role=cmd[3]
            u.phone = cmd[4]
            u.address = cmd[5]
            u.officeHours = cmd[6]
            u.officeHoursDates = cmd[7]

            for ch in cmd[7]:
                if valid_dates.intersection(ch):
                    continue
                else:
                    return 'Invalid date(s)'
            u.officeHoursDates = cmd[7]
            u.officeLocation = cmd[8]
            u.resume = cmd[9]
            u.schedule = cmd[10]
            u.preferences = cmd[11]
            
        else:
            return 'User does not exist'
        u.save()
        return 'User Updated'

    def edit_profile(self, cmd: [str]):
        u = self.currentUser
        if u:
            u.resume = cmd[0]
            u.schedule = cmd[1]
            u.preferences = cmd[2]
        u.save()
        return 'Profile updated'

    def create_user(self, cmd: [str]):
        if not self.currentUser or not self.currentUser.has_role(Role.Administrator):
            return 'Only an Administrator can create a user'
        if len(cmd) != 3:
            return 'Invalid number of parameters'
        u = User.objects.filter(email=cmd[0])
        if u:
            return 'User already exists'
        u = User(email=cmd[0], password=cmd[1], role=cmd[2])
        u.save()
        return 'User Added'

    def login(self, cmd: [str]):
        if len(cmd) != 2:
            return 'Invalid number of parameters'
        try:
            u = User.objects.get(email=cmd[0])
        except Exception:
            return 'Given email does not belong to an existing user'
        if u.password != '':
            if u.password == cmd[1]:
                self.currentUser = u
                return 'Logged in as %s' % cmd[0]
            else:
                return 'Invalid credentials'
        else:
            u.password = cmd[1]
            u.save()
            return 'Logged in as %s, your new password has been saved' % cmd[0]

    def logout(self, cmd: [str]):
        if len(cmd) != 0:
            return 'Invalid number of parameters'
        if not self.currentUser:
            return 'No user is logged in'
        self.currentUser = None
        return 'You Are Logged Out'

    def validate(self, cmd: [str]):
        if len(cmd) != 0:
            return 'Invalid number of parameters'
        courselist = Course.objects.all()
        for i in courselist:
            for j in courselist:
                # Check if there are any overlapping TAs for courses that occur over the same times.
                intersection = set(i.graderTAs.all()).intersection(set(j.graderTAs.all()))
                if len(intersection) != 0 and i.name != j.name and not i.isOnline() and not j.isOnline():
                    if i.getStartTime() <= j.getStartTime() <= i.getEndTime() or i.getStartTime() <= j.getEndTime() <= i.getEndTime():
                        return 'Error: Overlapping TAs found in conflicting courses time <' + i.name + '> and <' + j.name + '>.'
                    elif j.getStartTime() <= i.getStartTime() <= j.getEndTime() or j.getStartTime() <= i.getEndTime() <= j.getEndTime():
                        return 'Error: Overlapping TAs found in conflicting courses time <' + i.name + '> and <' + j.name + '>.'
        return 'TA assignments are valid'
