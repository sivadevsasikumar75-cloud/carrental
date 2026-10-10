from django.db import models
from datetime import date


class userreg(models.Model):
    fname = models.CharField(max_length=50)
    adds = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    ph_no = models.CharField(max_length=10)
    dob = models.DateField()
    adhno = models.ImageField(upload_to='images/')
    dls = models.ImageField(upload_to='images/')
    uname = models.CharField(max_length=50)
    pword = models.CharField(max_length=50)
    rights = models.CharField(max_length=50, default='U')


# ✅ MUST EXIST (IMPORTANT)
class vehicle_entry(models.Model):
    vno = models.CharField(max_length=50)
    vname = models.CharField(max_length=100)
    vprice = models.IntegerField()
    vcolor = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='images/')
    ftype = models.CharField(max_length=100)
    scapacity = models.IntegerField()
    rday = models.IntegerField()
    gps_ph = models.CharField(max_length=10)
    max_km = models.IntegerField()
    echarge = models.IntegerField()
    sdepo = models.IntegerField()
    features = models.CharField(max_length=500)
    status = models.CharField(max_length=50, default='Free')
    pnm = models.IntegerField(default=100)

    def __str__(self):
        return self.vname


# ✅ BOOKING
class newbooking(models.Model):
    bno = models.AutoField(primary_key=True)
    bdate = models.DateField(default=date.today)

    user = models.ForeignKey(userreg, on_delete=models.CASCADE, null=True)
    vehicle = models.ForeignKey(vehicle_entry, on_delete=models.CASCADE, null=True)

    cread = models.IntegerField()
    rday = models.IntegerField()
    max_km = models.IntegerField()
    erate = models.IntegerField()
    sdepo = models.IntegerField()

    rdate = models.DateField(null=True, blank=True)

    pread = models.IntegerField(default=0)
    totalkm = models.IntegerField(default=0)
    noofdays = models.IntegerField(default=0)
    ekm = models.IntegerField(default=0)

    charge = models.IntegerField(default=0)
    echarge = models.IntegerField(default=0)
    tcharge = models.IntegerField(default=0)

    paid = models.IntegerField(default=0)
    bal = models.IntegerField(default=0)

    cdno = models.CharField(max_length=50)
    cvv = models.CharField(max_length=50, default='xx')
    cowner = models.CharField(max_length=50, default='xx')

    status = models.CharField(max_length=50, default="On Rent")
    photo = models.CharField(max_length=500, default='x')

    def __str__(self):
        return f"Booking {self.bno}"


class feedback(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    feed = models.CharField(max_length=250)