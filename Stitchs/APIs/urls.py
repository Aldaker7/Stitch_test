from django.urls import path
from APIs import views

urlpatterns = [
    path('/api/board/<pk>',views.BoardListAPIView.as_view(),name='api'),
    path('/api/list/<pk>',views.ListListAPIView.as_view(),name='apilist'),
    path('/api/card/<pk>',views.CardListAPIView.as_view(),name='apicard'),
    path('/api/update/board/<pk>', views.BoardUpdateAPIView.as_view(), name='update_board'),
    path('/api/update/list/<pk>', views.ListUpdateAPIView.as_view(), name='update_list'),
    path('/api/update/card/<pk>', views.CardUpdateAPIView.as_view(), name='update_card'),
    path('/api/members', views.MembersListAPIView.as_view(), name='get_members'),
    path('/api/member/rename/<pk>', views.MemberUpdateAPIView.as_view(), name='api_rename'),
    path('/api/board/list/label/<pk>', views.LabelListAPIView.as_view(), name='get_labels_api'),
    path('/api/board/update/label/<pk>', views.LabelUpdateAPIView.as_view(), name='rename_label_api'),
]