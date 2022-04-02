from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name='apioverview'),
	# path('list/', views.ShowAll, name='list'),
	path('list/', views.UserViewSet.as_view({'get': 'list'}), name='list'),
	path('create/', views.createUser, name='create'),
	path('updatedb/', views.updateDB, name='update'),
	path('fetch/', views.fetchFromDB, name='fetch'),
]