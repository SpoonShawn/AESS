from django.urls import path

from . import views

app_name = 'grader'

urlpatterns = [
    path('', views.loging, name='login'),
    path('idex/', views.index, name='index'),
    path('<int:question_id>/', views.question, name='question'),
    path('<int:question_id>/essay<int:essay_id>/', views.essay, name='essay'),
    path('userlogin/',views.userlogin, name='userlogin'),
    path('logout/',views.userlogout, name='logout'),
    path('register/',views.register,name='register'),
    path('uinfo/',views.userInfo,name='userInfo'),
    path('uinfo/ucentre/',views.userCentre, name='userCentre'),
    path('changePassword/', views.changePassword, name='changePassword'),
    path('about/',views.about,name='about'),
    path('downloadfile/<int:doc_id>', views.download_file, name='download_file'),
    path('file2txt/', views.file2txt, name='file2txt'),
    path('chinese/', views.chinese, name='chinese'),
    path('zhessay<int:chinese_id>/', views.zhessay, name='zhessay')
]