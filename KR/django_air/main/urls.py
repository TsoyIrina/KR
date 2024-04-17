from django.urls import path, register_converter, re_path, include
from rest_framework import routers

from . import views
from .dt import DateConverter
from .views import RegisterUser, LoginUser, ShowProfile, EditProfile, ShowTicketPaid, ShowTicketUnpaid, Payment, \
    TicketDeleteView, TicketsAPIView, ProfilesAPIView, LoginAPIView

register_converter(DateConverter, 'date')

router_tick = routers.SimpleRouter()
router_tick.register(r'ticket', TicketsAPIView)

router_prof = routers.SimpleRouter()
router_prof.register(r'profile', ProfilesAPIView)

urlpatterns = [

    re_path(r'^\.(?P<confirm_ticket>[0-1]?)/?$', views.index, name='main'),
    path('', views.index, name='main'),
    path('search/', views.search_tick, name='search_tick'),

    path('test_search/<slug:tick_from_slug>/<slug:tick_to_slug>/<int:id>/', views.who_air_v, name='who'),
    path('test_search/<slug:tick_from_slug>/<slug:tick_to_slug>/<int:id>/<date:date>/<int:ad>/<int:ch>/<int:inf>',
         views.res_tick, name='ticket'),
    path('search/ticket/<slug:tick_from_slug>/<slug:tick_to_slug>/', views.res, name='res'),

    path('register/', RegisterUser.as_view(), name='reg'),
    path('login/', LoginUser.as_view(), name='log'),
    path('logout/', views.logout_user, name='logout'),

    path('profile/<str:username>/', ShowProfile.as_view(), name='profile'),
    path('edit/<str:username>/', EditProfile.as_view(), name='edit'),

    path('ticket_unpaid/<str:username>/', ShowTicketUnpaid.as_view(), name='tick_unpaid'),
    path('ticket_paid/<str:username>/', ShowTicketPaid.as_view(), name='tick_paid'),

    path('payment/<int:pk>/', Payment.as_view(), name='payment'),
    path('delete/<int:pk>/', TicketDeleteView.as_view(), name='tick_del'),

    path('api/v1/', include(router_tick.urls)),
    path('api/v1/', include(router_prof.urls)),

    path('api/v1/drf-auth/', include('rest_framework.urls')),

    path('api/v1/login/', LoginAPIView.as_view()),
]
