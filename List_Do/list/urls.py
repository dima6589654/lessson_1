"""
URL configuration for List_Do project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from list.views import AddList,ReadList,ListDo,UpdateList,DeleteList

urlpatterns = [
    path('addlist/', AddList.as_view(), name='add_list'),
    path('readlist/<int:pk>/', ReadList.as_view(), name='read_list'),
    path('', ListDo.as_view(), name='list_do'),
    path('deleteList/<int:pk>/', DeleteList.as_view(), name='delete_list'),
    path('updatesms/<int:pk>/', UpdateList.as_view(), name='update_sms'),
]