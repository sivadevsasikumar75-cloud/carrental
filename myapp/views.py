from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.functions import Coalesce
from django.db.models import Max, Value
from datetime import date, datetime
from functools import wraps
import math

from .models import userreg, vehicle_entry, newbooking, feedback


# ==============================================================================
# 🔐 AUTHENTICATION DECORATORS
# ==============================================================================

def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' not in request.session:
            return redirect('login')

        response = view_func(request, *args, **kwargs)

        # 🔥 Force no cache
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
    return wrapper


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'id' not in request.session or request.session.get('rights') != 'A':
            return redirect('login')

        response = view_func(request, *args, **kwargs)

        # 🔥 Force no cache
        response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
    return wrapper


# ==============================================================================
# 🏠 PUBLIC & USER VIEWS
# ==============================================================================

def homepage(request):
    """Landing page: Displays customer feedback and available vehicles."""
    frec = feedback.objects.all()
    crec = vehicle_entry.objects.filter(status='Free')[:8]
    return render(request, "index.html", {"frec": frec, "crec": crec})


def adduserreg(request):
    """User Registration: Handles file uploads for ID and License."""
    if request.method == "POST":
        userreg.objects.create(
            fname=request.POST.get('fname'),
            adds=request.POST.get('adds'),
            email=request.POST.get('email'),
            ph_no=request.POST.get('ph_no'),
            dob=request.POST.get('dob'),
            adhno=request.FILES.get('adhno'),
            dls=request.FILES.get('dls'),
            uname=request.POST.get('uname'),
            pword=request.POST.get('pword'),
            rights='U'
        )
        return redirect("/mi/")
    return render(request, "uregistration.html")


def loginpage(request):
    """Login logic: Sets session variables for name, email, and rights."""
    if request.method == "POST":
        u = request.POST.get('u')
        p = request.POST.get('p')
        user = userreg.objects.filter(uname=u, pword=p).first()

        if user:
            request.session['id'] = user.id
            request.session['name'] = user.fname
            request.session['phone'] = user.ph_no
            request.session['email'] = user.email
            request.session['rights'] = user.rights

            if user.rights == "A":
                return redirect("/ap/")
            else:
                return redirect("/up/")
        else:
            return render(request, "login.html", {"error": "Invalid Username or Password"})
    return render(request, "login.html")


def logoutpage(request):
    request.session.flush()
    response = redirect('homepage')

    # 🔥 clear cache after logout
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'

    return response


@login_required
def userpage(request):
    """User Dashboard: Shows list of free vehicles for booking."""
    crec = vehicle_entry.objects.filter(status='Free')
    return render(request, "userpage.html", {
        "crec": crec,
        "name": request.session.get('name')
    })


# ==============================================================================
# 🚗 BOOKING & PAYMENT FLOW
# ==============================================================================

@login_required
def carbooking(request, id):
    """Booking Initiation: Prepares booking number and displays vehicle specs."""
    request.session['vid'] = id
    vrec = get_object_or_404(vehicle_entry, id=id)

    # Calculate next booking number
    max_bno = newbooking.objects.aggregate(max_bno=Coalesce(Max('bno'), Value(0)))['max_bno']
    mbno = int(max_bno) + 1

    return render(request, "userbooking.html", {
        "mbno": mbno,
        "cdate": date.today(),
        "name": request.session.get('name'),
        "phone": request.session.get('phone'),
        "email": request.session.get('email'),
        "vrec": vrec
    })


@login_required
def paynow(request):
    """Payment Gateway Simulation: Stores start KM in session."""
    vid = request.session.get('vid')
    vrec = get_object_or_404(vehicle_entry, id=vid)

    if request.method == "POST":
        request.session['temp_cread'] = request.POST.get('cread')
        request.session['temp_bno'] = request.POST.get('bno')

    return render(request, "paynow.html", {"bamt": vrec.sdepo})


@login_required
def updatebooking(request):
    """Finalizes booking: Saves to database."""
    if request.method == "POST":
        cno = request.POST.get('cno')

        # We only check if the field is empty now
        if not cno:
            # Need to pass bamt back if there is an error
            vid = request.session.get('vid')
            vrec = get_object_or_404(vehicle_entry, id=vid)
            return render(request, "paynow.html", {"error": "Card number is required", "bamt": vrec.sdepo})

        user_obj = get_object_or_404(userreg, id=request.session.get('id'))
        vehicle_obj = get_object_or_404(vehicle_entry, id=request.session.get('vid'))

        newbooking.objects.create(
            bno=request.session.get('temp_bno'),
            bdate=date.today(),
            user=user_obj,
            vehicle=vehicle_obj,
            cread=int(request.session.get('temp_cread', 0)),
            rday=vehicle_obj.rday,
            max_km=vehicle_obj.max_km,
            erate=vehicle_obj.echarge,
            sdepo=vehicle_obj.sdepo,
            cdno=cno,
            photo=vehicle_obj.photo,
            status="On Rent"
        )

        # Mark car as unavailable
        vehicle_obj.status = "On Rent"
        vehicle_obj.save()

        return redirect('/up/')

@login_required
def userviewbooking(request):
    """Allows users to see their active and past rental history."""
    rec = newbooking.objects.filter(user__id=request.session.get('id'))
    return render(request, "viewuserbooking.html", {"rec": rec})


# ==============================================================================
# 🔧 ADMIN MANAGEMENT (FULL VEHICLE CONTROL)
# ==============================================================================

@admin_required
def adminpage(request):
    """Admin Dashboard Home."""
    return render(request, "adminpage.html")


@admin_required
def addvehicle(request):
    """Admin: Add new vehicle to inventory."""
    if request.method == "POST":
        vehicle_entry.objects.create(
            vno=request.POST.get('vno'),
            vname=request.POST.get('vname'),
            vprice=request.POST.get('vprice'),
            vcolor=request.POST.get('vcolor'),
            photo=request.FILES.get('photo'),
            ftype=request.POST.get('ftype'),
            scapacity=request.POST.get('scapacity'),
            rday=request.POST.get('rday'),
            gps_ph=request.POST.get('gps_ph'),
            max_km=request.POST.get('max_km'),
            echarge=request.POST.get('echarge'),
            sdepo=request.POST.get('sdepo'),
            features=request.POST.get('features'),
            status='Free'
        )
        return redirect('/lms/')
    return render(request, "adminaddvehicles.html")


@admin_required
def listvehicle(request):
    """Admin: List all vehicles with edit/delete options."""
    crec = vehicle_entry.objects.all()
    return render(request, "adminvehiclelist.html", {"crec": crec})


@admin_required
def editvehicle(request, id):
    """Admin: Edit existing vehicle details."""
    vehicle = get_object_or_404(vehicle_entry, id=id)
    if request.method == "POST":
        vehicle.vno = request.POST.get('vno')
        vehicle.vname = request.POST.get('vname')
        vehicle.vprice = request.POST.get('vprice')
        vehicle.vcolor = request.POST.get('vcolor')
        vehicle.ftype = request.POST.get('ftype')
        vehicle.scapacity = request.POST.get('scapacity')
        vehicle.rday = request.POST.get('rday')
        vehicle.gps_ph = request.POST.get('gps_ph')
        vehicle.max_km = request.POST.get('max_km')
        vehicle.echarge = request.POST.get('echarge')
        vehicle.sdepo = request.POST.get('sdepo')
        vehicle.features = request.POST.get('features')

        if 'photo' in request.FILES:
            vehicle.photo = request.FILES['photo']

        vehicle.save()
        return redirect('/lms/')
    return render(request, "admineditvehicles.html", {"vehicle": vehicle})


@admin_required
def delprogram(request, id):
    """Admin: Delete a vehicle from the system."""
    vehicle_entry.objects.filter(id=id).delete()
    return redirect("/lms/")


@admin_required
def ourcustomers(request):
    """Admin: View all registered customers."""
    rec = userreg.objects.all()
    return render(request, "admincustomer.html", {"rec": rec})


@admin_required
def adminviewbooking(request):
    """Admin: View cars currently out on rent."""
    rec = newbooking.objects.filter(status='On Rent')
    return render(request, "adminbookinglist.html", {"rec": rec})


@admin_required
def arrivals(request, id):
    rec = get_object_or_404(newbooking, bno=id)

    if request.method == "POST":
        try:
            # handle '0.00' decimal strings from frontend
            rec.pread = int(float(request.POST.get('pread', 0)))
            rec.totalkm = int(float(request.POST.get('kms', 0)))
            rec.ekm = int(float(request.POST.get('ekm', 0)))
            rec.echarge = int(float(request.POST.get('echarge', 0)))
            rec.tcharge = int(float(request.POST.get('tcharge', 0)))
            rec.bal = int(float(request.POST.get('bal', 0)))

            rec.rdate = date.today()
            rec.status = "Closed"
            rec.vehicle.status = "Free"
            rec.vehicle.save()
            rec.save()
            return redirect('/abl/')
        except (ValueError, TypeError):
            pass

    # --- DURATION FIX ---
    delta = (date.today() - rec.bdate).days

    # If the difference is 0 (same day), force it to 1.
    # If it is 1 or more, it stays as is.
    current_nod = delta if delta > 0 else 1

    daily_rate = int(float(rec.rday))
    base_rent_charge = current_nod * daily_rate

    context = {
        "bno": rec.bno,
        "vno": rec.vehicle.vno,
        "vname": rec.vehicle.vname,
        "nod": current_nod,  # THIS MUST BE SENT AS 'nod'
        "rday": daily_rate,
        "charge": base_rent_charge,
        "cread": rec.cread,
        "max_km": rec.max_km,
        "erate": rec.erate,
        "sdepo": rec.sdepo
    }
    return render(request, "adminrentclosing.html", context)

@admin_required
def adminbookinghistory(request):
    """Admin: View all closed transactions."""
    rec = newbooking.objects.filter(status='Closed')
    return render(request, "adminbookinghistory.html", {"rec": rec})

# ==============================================================================
# ⚙️ UTILITY & PROFILE VIEWS
# ==============================================================================

@login_required
def userfeedback(request):
    """Users can submit feedback; auto-populates name/phone from session."""
    if request.method == "POST":
        feedback.objects.create(
            name=request.POST.get('em'),  # Name field used for Email per template
            phone=request.POST.get('ph'),
            feed=request.POST.get('fd')
        )
        return redirect('/up/')

    return render(request, "feedback.html", {
        "name": request.session.get('email'),
        "phone": request.session.get('phone')
    })


@login_required
def changepword(request):
    """Allows users to update their password after verifying current one."""
    if request.method == "POST":
        old = request.POST.get('t1')
        new = request.POST.get('t2')
        confirm = request.POST.get('t3')
        user = get_object_or_404(userreg, id=request.session.get('id'))

        if user.pword == old:
            if new == confirm:
                user.pword = new
                user.save()
                request.session.flush()  # Force logout after password change
                return redirect('/mi/')
            else:
                return render(request, "changepword.html", {"error": "New passwords do not match"})
        else:
            return render(request, "changepword.html", {"error": "Current password is incorrect"})

    return render(request, "changepword.html")