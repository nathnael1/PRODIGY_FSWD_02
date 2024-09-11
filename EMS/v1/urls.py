from django.urls import path

from . import views
urlpatterns = [
    path("",views.index, name = "index"),
    path("register",views.register,name = "register"),
    path("login",views.login,name = "login"),
    path("edit",views.edit,name = "edit"),
    path("adminmanager",views.adminmanager,name = "adminmanager"),
]
