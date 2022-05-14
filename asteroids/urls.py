from django.urls import path

from asteroids import views

urlpatterns = [
    path('', views.getDates, name='getDates'),
    path('<str:start_date>/', views.getDates),
    path('/<str:end_date>', views.getDates),
    path('<str:start_date>/<str:end_date>', views.getDates),
]
