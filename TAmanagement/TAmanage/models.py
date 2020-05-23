from enum import IntEnum

from django.db import models
from datetime import datetime


class Role(IntEnum):
    TA = 1
    Instructor = 2
    Administrator = 3


class User(models.Model):
    email = models.CharField(max_length=50, blank=False, null=False)
    password = models.CharField(max_length=100, blank=False, null=False)
    firstName = models.CharField(max_length=50, default='None', blank=True, null=True)
    lastName = models.CharField(max_length=50, default='None', blank=True, null=True)
    phone = models.CharField(max_length=15, default='None', blank=True, null=True)
    address = models.CharField(max_length=255, default='None', blank=True, null=True)
    officeHours = models.CharField(max_length=15, default='None', blank=True, null=True)
    officeHoursDates = models.CharField(max_length=6, default='None', blank=True, null=True)
    officeLocation = models.CharField(max_length=255, default='None', blank=True, null=True)
    role = models.SmallIntegerField(default=1)
    resume = models.CharField(max_length=5000, blank=True, null=True)
    schedule = models.CharField(max_length=5000, blank=True, null=True)
    preferences = models.CharField(max_length=5000, blank=True, null=True)

    def has_role(self, *roles: [Role]) -> bool:
        return Role(self.role) in roles

    def userEmail(self):
        return self.email

    def __str__(self):
        return self.userEmail()


class Lab(models.Model):
    location = models.CharField(max_length=255, null=True, blank=True, default="Online")
    section = models.CharField(max_length=20, default='000')

    # Start and End Times for Each Lab
    startTime = models.TimeField('Start Time:', default=datetime.now, blank=True, null=True)
    endTime = models.TimeField('End Time:', default=datetime.now, blank=True, null=True)

    # Date Field for Dates, if it's online, it is "Online" instead of a combination of M, T, W, R, F, or S
    # Date cannot include Sundays, as classes are not on Sundays
    dates = models.CharField(max_length=6, default='MTWRFS', blank=False, null=False)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    ta = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)


class Course(models.Model):
    instructor = models.ForeignKey("User", null=True, blank=True, on_delete=models.SET_NULL)
    # Each course has a name
    name = models.CharField(max_length=20, default='CS000')
    section = models.CharField(max_length=20, default='000', null=False, blank=False)
    location = models.CharField(max_length=255, default='Online', null=True, blank=True)

    # Start and End Times for Each Course
    startTime = models.TimeField('Start Time:', default=datetime.now, null=True, blank=True)
    endTime = models.TimeField('End Time:', default=datetime.now, null=True, blank=True)

    # Date Field for Dates, if it's online, it is "Online" instead of a combination of M, T, W, R, F, or S
    # Date cannot include Sundays, as classes are not on Sundays
    dates = models.CharField(max_length=6, default='MTWRFS', blank=False, null=False)
    graderTAs = models.ManyToManyField("User", blank=True, related_name='courses')

    # Return the course name
    def courseName(self):
        return self.name

    # Check if a course is online or not
    def isOnline(self):
        return self.dates == 'Online'

    # Getter method for startTime
    def getStartTime(self):
        if self.dates == "Online":
            return None
        return self.startTime

    def setStartTime(self, start):
        self.startTime = start

    # Getter method for endTime
    def getEndTime(self):
        if self.dates == "Online":
            return None
        return self.endTime

    def setEndTime(self, end):
        self.endTime = end

    # Getter method for dates
    def getDates(self):
        return self.dates

    def setDates(self, dates):
        self.dates = dates

    def __str__(self):
        return self.courseName()
