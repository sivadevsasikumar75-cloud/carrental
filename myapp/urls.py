from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('h/', views.homepage, name='home'),

    path('adp/', views.addvehicle, name='addvehicle'),
    path('lms/', views.listvehicle, name='listvehicle'),
    path('tyu/', views.adduserreg, name='adduserreg'),
    path('lc/', views.ourcustomers, name='ourcustomers'),

    path('mi/', views.loginpage, name='login'),
    path('logout/', views.logoutpage, name='logout'),

    path('ap/', views.adminpage, name='adminpage'),
    path('up/', views.userpage, name='userpage'),   # ✅ FIXED

    path('cp/', views.changepword, name='changepword'),

    path('dms/<int:id>/', views.delprogram, name='deletevehicle'),
    path('ems/<int:id>/', views.editvehicle, name='editvehicle'),

    path('bnow/<int:id>/', views.carbooking, name='carbooking'),

    path('paynow/', views.paynow, name='paynow'),   # ✅ ADDED
    path('pays/', views.updatebooking, name='updatebooking'),

    path('uvb/', views.userviewbooking, name='userviewbooking'),
    path('abl/', views.adminviewbooking, name='adminviewbooking'),
    path('abh/', views.adminbookinghistory, name='adminbookinghistory'),

    path('arr/<int:id>/', views.arrivals, name='arrivals'),

    path('fd/', views.userfeedback, name='userfeedback'),
]