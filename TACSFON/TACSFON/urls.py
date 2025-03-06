
from django.contrib import admin
from django.urls import path
from TACSFON_APP import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('add/', views.add_contact, name='add_contact'),
    # path('index', views.index, name='index'),
    # path('upload/', views.upload_csv, name='upload_csv'),
    # path('add-new-contacts/', views.add_new_contacts, name='add_new_contacts'),
    path('', views.index, name='index'),
    path('add/', views.add_contact, name='add_contact'),
    path('upload/', views.upload_excel, name='upload_excel'),
    path('add-new-contacts/', views.add_new_contacts, name='add_new_contacts'),
]


