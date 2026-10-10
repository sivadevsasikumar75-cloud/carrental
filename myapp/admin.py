from django.contrib import admin
from myapp.models import userreg, vehicle_entry, newbooking


# 🔹 User Registration Admin
class userregadmin(admin.ModelAdmin):
    list_display = (
        'id', 'fname', 'adds', 'email', 'ph_no',
        'dob', 'adhno', 'dls', 'uname', 'pword', 'rights'
    )


# 🔹 Vehicle Admin
class vehicle_entryadmin(admin.ModelAdmin):
    list_display = (
        'id', 'vno', 'vname', 'vprice', 'vcolor',
        'photo', 'ftype', 'scapacity', 'rday',
        'gps_ph', 'max_km', 'echarge', 'sdepo', 'status'
    )


# 🔹 Booking Admin (UPDATED ✅)
class newbookingadm(admin.ModelAdmin):
    list_display = (
        'bno', 'bdate',
        'user', 'vehicle',
        'cread', 'rday', 'max_km',
        'erate', 'sdepo',
        'rdate',
        'charge', 'echarge', 'tcharge',
        'paid', 'bal',
        'status'
    )


# 🔹 Register Models
admin.site.register(userreg, userregadmin)
admin.site.register(vehicle_entry, vehicle_entryadmin)
admin.site.register(newbooking, newbookingadm)