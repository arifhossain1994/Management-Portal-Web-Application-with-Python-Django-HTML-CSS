"""TAmanagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from TAmanage import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    path('createCourse', views.CreateCourse.as_view()),
    path('createUser', views.CreateUser.as_view()),
    path('', views.Home.as_view()),
    path('login/', views.Login.as_view()),
    path('logout', views.Logout.as_view()),
    path('editCourse', views.EditCourse.as_view()),
    path('listCourses', views.ListCourses.as_view()),
    path('listUsers', views.ListUsers.as_view()),
    #path('editProfile', views.EditProfile.as_view()),
    path('editUser', views.EditUser.as_view()),
    path('viewProfile', views.ViewProfile.as_view()),
    path('viewUser', views.ViewUser.as_view()),
    path('deleteCourse', views.DeleteCourse.as_view()),
    path('assignTas', views.AssignTa.as_view()),
    path('deleteUser', views.DeleteUser.as_view()),
    path('createLab', views.CreateLab.as_view()),
    path('editLab', views.EditLab.as_view()),
    path('viewLabs', views.ViewLabs.as_view()),
    path('validateCourse', views.Validate.as_view()),
]

