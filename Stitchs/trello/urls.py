from django.urls import path
from trello import views

urlpatterns = [
    path('', views.login_user, name='login'),
    path('logout',views.logout_user,name='logout'),
    path('signup',views.signup_user,name='signup'),
    path('boards',views.get_user_board,name='boards'),
    path('create', views.create_board, name='create'),
    path('lists/8?46221<pk>125/<order>1',views.get_list,name='list'),
    path('createlists/<pk>', views.create_list, name='create_list'),
    path('cards/<pk>/<order>', views.get_card, name='cards'),
    path('createards/<list_id>', views.create_card, name='create_card'),
    path('archivelist/<pk>',views.archive_list,name='archive_list'),
    path('archivecard/<pk>',views.archive_card,name='archive_card'),
    path('archiveboard/<pk>',views.archive_board,name='archive_board'),
    path('api/updates/board/<pk>', views.updates_board, name='updates_board'),
    path('api/updates/list/<pk>', views.updates_list, name='updates_list'),
    path('api/updates/card/<pk>', views.updates_card, name='updates_card'),
    path('create/member', views.create_member, name='create_member'),
    path('listmember', views.get_members, name='list_members'),
    path('member/rename/<pk>', views.rename_member, name='rename_member'),
    path('member/archive/<pk>', views.archive_member, name='archive_member'),
    path('board/labels/<pk>', views.get_labels, name='get_labels'),
    path('board/rename/label/<pk>', views.rename_label, name='rename_label'),
    path('board/archive/label/<pk>', views.archive_label, name='archive_label'),

]