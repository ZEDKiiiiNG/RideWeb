from django.urls import path

# urlpatterns = [
#     # ex: /polls/
#     path('', views.index, name='index'),
#     # ex: /polls/5/
#     path('<int:question_id>/', views.detail, name='detail'),
#     # ex: /polls/5/results/
#     path('<int:question_id>/results/', views.results, name='results'),
#     # ex: /polls/5/vote/
#     path('<int:question_id>/vote/', views.vote, name='vote'),
# ]

from . import views


urlpatterns = [
    # ex: /polls/
    path('index/', views.index, name='index'),
    # ex: /polls/5/
    path('login/', views.login, name='login'),
    # ex: /polls/5/results/
    path('register/', views.register, name='register'),
    # ex: /polls/5/vote/
    path('logout/', views.logout, name='logout'),
]