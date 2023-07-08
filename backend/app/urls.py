from django.urls import path, include
from .views import views

from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

urlpatterns = [
	path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
	path('', views.index, name='index'),
	path('politica', views.politica, name='politica'),
	path('root/', views.LevelListView.as_view(), name='root'),
	path('root/detail/<int:id>/', views.detail, name='detail'),
	path('root/getfile/<int:id>/', views.get_file, name='get_file'),
	path('root/search/', views.search, name='search'),
	path('download-app/<str:name>/', views.download_app, name='get_app'),
	path('click/<str:name>/', views.get_click, name='get_click'),
]
