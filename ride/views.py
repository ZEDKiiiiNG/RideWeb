from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
#
# def detail(request, question_id):
#     return HttpResponse("You're looking at question %s." % question_id)
#
# def results(request, question_id):
#     response = "You're looking at the results of question %s."
#     return HttpResponse(response % question_id)
#
# def vote(request, question_id):
#     return HttpResponse("You're voting on question %s." % question_id)

from django.shortcuts import render,redirect
from .forms import UserForm,RegisterForm,DriverRigisterForm, RideForm,passengerSearchRideForm, JointRideForm
from . import models
from django.db.models import Q
from django.core.mail import send_mail
from RideWeb.settings import EMAIL_HOST_USER

def jointEditRide(request):
    if not request.session.get('is_login', None):
        message = "Please log in first！"
        return render(request, 'login/login.html', locals())
    joint_ride_form = JointRideForm()
    ride_edit_id = request.session.get('joint_ride_edit_id', None)
    #TODO 前面部分要不要也改id写法
    ride_item = models.Ride.objects.get(id = ride_edit_id)
    if request.method == "POST" and request.POST:
        joint_ride_form = JointRideForm(request.POST)
        if joint_ride_form.is_valid():
            joint_sharer = ride_item.sharer.all()
            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)
            sharer = joint_sharer.get(owner= user)
            sharer.partySize = joint_ride_form.cleaned_data["partySize"]
            sharer.save()
            ride_item.save()
            return redirect('/passenger')
        else:
            message = 'please check the input format'
            return render(request, "login/jointEditRide.html", locals())
    return render(request, "login/jointEditRide.html", locals())


def passengerSearchRide(request):
    if not request.session.get('is_login', None):
        message = "Please log in first！"
        return render(request, 'login/login.html', locals())
    pass_search_form  = passengerSearchRideForm()
    if request.method == "GET" and request.GET:
        if 'go back' in request.GET:
            return redirect("/passenger/")
        if 'Join' in request.GET:
            ride_join_id = request.GET.get('Join')
            #TODO
            ride_item = models.Ride.objects.get(id=ride_join_id)
            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)
            user_party_size = request.session.get('partySize',0)
            new_sharar = models.JoinRide(owner=user, partySize= user_party_size)
            new_sharar.save()
            ride_item.sharer.add(new_sharar)
            message = "successfully join the ride"
            return redirect("/passenger/")
    if request.method == "POST" and request.POST:
        pass_search_form = passengerSearchRideForm(request.POST)
        if pass_search_form.is_valid():
            #user cannot be the owner
            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)
            end = pass_search_form.cleaned_data["end"]
            earlyArrivalDate = pass_search_form.cleaned_data["earlyArrivalDate"]
            earlyArrivalTime = pass_search_form.cleaned_data["earlyArrivalTime"]
            lateArrivalDate = pass_search_form.cleaned_data["lateArrivalDate"]
            lateArrivalTime = pass_search_form.cleaned_data["lateArrivalTime"]
            partySize = pass_search_form.cleaned_data["partySize"]
            #save the party size
            request.session['partySize'] = partySize
            ride_list_notowner = models.Ride.objects.exclude(owner= user)
            ride_list_open = ride_list_notowner.filter(status = 'open')
            ride_list_share = ride_list_open.filter(isSharable = True)
            ride_list_end = ride_list_open.filter(end = end)
            #TODO 看看有没有其他写法
            ride_list_date = ride_list_end.filter(date__range= (earlyArrivalDate,lateArrivalDate) )
            # ride_list_final = ride_list_date.filter(time__lte=lateArrivalTime, time__gte=earlyArrivalTime)
            ride_list_time = ride_list_date.exclude(Q(date=earlyArrivalDate) & Q(time__lt = earlyArrivalTime) )
            ride_list_final = ride_list_time.exclude(Q(date=lateArrivalDate) & Q(time__gt=lateArrivalTime))

            return render(request, "login/passengerSearchRide.html", locals())
    return render(request, "login/passengerSearchRide.html", locals())

def editRide(request):
    if not request.session.get('is_login', None):
        message = "Please log in first！"
        return render(request, 'login/login.html', locals())
    ride_form = RideForm()
    ride_edit_id = request.session.get('ride_edit_id', None)
    #TODO 前面部分要不要也改id写法
    ride_item = models.Ride.objects.get(id = ride_edit_id)
    if request.method == "POST" and request.POST:
        ride_form = RideForm(request.POST)
        if ride_form.is_valid():
            ride_item.end = ride_form.cleaned_data["end"]
            # start to make sure driver know where to pick
            ride_item.start = ride_form.cleaned_data["start"]
            ride_item.date = ride_form.cleaned_data["arrivalDate"]
            ride_item.time = ride_form.cleaned_data["arrivalTime"]
            ride_item.partySize = ride_form.cleaned_data["partySize"]
            ride_item.specialRequests = ride_form.cleaned_data["specialRequests"]
            ride_item.vehicleTypeRequest = ride_form.cleaned_data["vehicleTypeRequest"]
            ride_item.isSharable = ride_form.cleaned_data["isSharable"]


            ride_item.save()
            return redirect('/passenger')
        else:
            message = 'please check the input format'
            return render(request, "login/editRide.html", locals())
    return render(request, "login/editRide.html", locals())


def passengerPage(request):
    if not request.session.get('is_login', None):
        message = "Please log in first！"
        # if already signed in, then cannot register
        # return redirect("/login/")
        #TODO 怎么让views也进入login
        return render(request, 'login/login.html', locals())

    username = request.session.get('user_name', None)
    user = models.User.objects.get(name=username)
    rideList = user.ride_set.all()
    rideJoinedList = models.Ride.objects.filter(sharer__owner= user)
    if 'create ride' in request.GET:
        return redirect("/createRide")
    if 'Edit' in request.GET:
        ride_edit_id = request.GET.get('Edit')
        request.session['ride_edit_id'] = ride_edit_id
        return redirect("/editRide")
    if 'search ride' in request.GET:
        return redirect("/passengerSearchRide")
    if 'joint Edit' in request.GET:
        ride_edit_id = request.GET.get('joint Edit')
        request.session['joint_ride_edit_id'] = ride_edit_id
        return redirect("/jointEditRide")

    # user = models.User.objects.get(name=request.session['user_name'])
    # rideList = models.Ride.objects.filter(owner=user)

    return render(request, "login/passenger.html", locals())

def createRide(request):
    ride_form = RideForm()
    if request.method == "POST" and request.POST:
        ride_form = RideForm(request.POST)
        if ride_form.is_valid():
            end = ride_form.cleaned_data["end"]
            # start to make sure driver know where to pick
            start = ride_form.cleaned_data["start"]
            arrivalDate = ride_form.cleaned_data["arrivalDate"]
            arrivalTime = ride_form.cleaned_data["arrivalTime"]
            partySize = ride_form.cleaned_data["partySize"]
            specialRequests = ride_form.cleaned_data["specialRequests"]
            vehicleTypeRequest = ride_form.cleaned_data["vehicleTypeRequest"]
            isSharable = ride_form.cleaned_data["isSharable"]

            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)

            newRide = models.Ride(owner=user, date=arrivalDate, time=arrivalTime, start=start, end=end,
                             partySize=partySize, specialRequests=specialRequests, isSharable=isSharable, vehicleTypeRequest= vehicleTypeRequest)

            newRide.save()
            return redirect('/passenger')
        else:
            message = 'please check the input format'
            return render(request, "login/createRide.html", locals())
    ride_form = RideForm()
    newRide = models.Ride.objects.all
    return render(request, "login/createRide.html", locals())

def driverEdit(request):
    if not request.session['is_driver']:
        message = "Please register as a driver first ！"
        return redirect('/driverRegister/')
    #in case redirect and cannot display drievr information
    #TODO check set structre
    driver_register_form = DriverRigisterForm()
    username = request.session.get('user_name', None)
    user = models.User.objects.get(name=username)
    # driver_set = user.driver_set.all()
    # unique owner for every driver
    driver_self = models.Driver.objects.get(owner = user)

    if request.method == "POST":
        driver_register_form = DriverRigisterForm(request.POST)
        message = "Please check the content！"
        if driver_register_form.is_valid():  # get the detaile data
            vehicleType = driver_register_form.cleaned_data['vehicleType']
            licensePlateNumber = driver_register_form.cleaned_data['licensePlateNumber']
            allowedPassengers = driver_register_form.cleaned_data['allowedPassengers']
            specialInfo = driver_register_form.cleaned_data['specialInfo']



            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)
            #TODO 检查逻辑
            # if request.session.get('is_driver', None):
            #     # if already is driver, then just addit
            #
            #when already a driver then cannot have drive info
            driver = models.Driver.objects.get(owner=user)
            same_licensePlateNumber = models.Driver.objects.filter(licensePlateNumber=licensePlateNumber)
            if same_licensePlateNumber and licensePlateNumber != driver.licensePlateNumber:  # found the same same_licensePlateNumber
                message = 'licensePlateNumber already exists！'
                return render(request, 'login/driverEdit.html', locals())
            driver.vehicleType = vehicleType
            driver.licensePlateNumber = licensePlateNumber
            driver.allowedPassengers = allowedPassengers
            driver.specialInfo = specialInfo
            driver.save()

            return redirect('/Driver/')



    return render(request, "login/driverEdit.html", locals())


def driverPage(request):
    if not request.session.get('is_login', None):
        message = "Please log in first！"
        # if already signed in, then cannot register
        # return redirect("/login/")
        #TODO 怎么让views也进入login
        return render(request, 'login/login.html', locals())
    if not request.session.get('is_driver', None):
        message = "Please register as a driver first ！"
        return redirect('/driverRegister/')


    username = request.session.get('user_name', None)
    user = models.User.objects.get(name=username)
    # driver_set = user.driver_set.all()
    # unique owner for every driver
    driver_self = models.Driver.objects.get(owner=user)
    ride_list = models.Ride.objects.filter(driver__owner = user)
    ride_list_confirmed = ride_list.filter(status= 'confirmed')

    #search part:
    from django.db.models import Sum
    ride_open = models.Ride.objects.filter(status= 'open')
    ride_vehicle = ride_open.filter(vehicleTypeRequest= driver_self.vehicleType)
    ride_available_list = ride_vehicle.filter(specialRequests= driver_self.specialInfo)
    for ride in ride_vehicle.all():
        ride_id = ride.id
        total_passenger_num = ride.partySize
        for share in ride.sharer.all():
            total_passenger_num += share.partySize
        if total_passenger_num > driver_self.allowedPassengers:
            ride_available_list = ride_available_list.exclude(id = ride_id)

    if request.method == "GET" and request.GET:
        if 'Edit' in request.GET:
            return redirect('/driverEdit/')
        if 'Complete' in request.GET:
            ride_confirmed_id  = request.GET.get('Complete')
            ride_item = models.Ride.objects.get(id = ride_confirmed_id)
            ride_item.status = 'complete'
            ride_item.save()
        if 'Confirmed' in request.GET:
            ride_confirmed_id  = request.GET.get('Confirmed')
            ride_item = models.Ride.objects.get(id = ride_confirmed_id)
            ride_item.driver = driver_self
            ride_item.status = 'confirmed'
            ride_owner_email = ride_item.owner.email
            ride_email = []
            ride_email.append(str(ride_owner_email))
            for shar in ride_item.sharer.all():
                ride_email.append(str(shar.owner.email))
            #send email
            send_mail(
                subject='Ride Confirmed',
                message = 'Your ride has already been confrimed',
                from_email= EMAIL_HOST_USER,
                recipient_list = ride_email,
                fail_silently= False
            )


            ride_item.save()
    return render(request, 'login/driverPage.html', locals())


def driverRegister(request):

    if request.session.get('is_driver', None):
        return redirect('/Driver/')
    if request.method == "POST":
        driver_register_form = DriverRigisterForm(request.POST)
        message = "Please check the content！"
        if driver_register_form.is_valid():  # get the detaile data
            vehicleType = driver_register_form.cleaned_data['vehicleType']
            licensePlateNumber = driver_register_form.cleaned_data['licensePlateNumber']
            allowedPassengers = driver_register_form.cleaned_data['allowedPassengers']
            specialInfo = driver_register_form.cleaned_data['specialInfo']

            same_licensePlateNumber = models.Driver.objects.filter(licensePlateNumber=licensePlateNumber)
            if same_licensePlateNumber:  # found the same same_licensePlateNumber
                message = 'licensePlateNumber already exists！'
                return render(request, 'login/driverRegister.html', locals())

            username = request.session.get('user_name', None)
            user = models.User.objects.get(name=username)
            #TODO 检查逻辑
            # if request.session.get('is_driver', None):
            #     # if already is driver, then just addit
            #
            #     #when already a driver then cannot have drive info
            #     driver = models.Driver.objects.get(owner=user)
            #     driver.vehicleType = vehicleType
            #     driver.licensePlateNumber = licensePlateNumber
            #     driver.allowedPassengers = allowedPassengers
            #     driver.specialInfo = specialInfo
            # else:
            #     driver = models.Driver(owner=user, vehicleType=vehicleType, licensePlateNumber=licensePlateNumber,
            #                          allowedPassengers=allowedPassengers, specialInfo=specialInfo)
            driver = models.Driver(owner=user, vehicleType=vehicleType, licensePlateNumber=licensePlateNumber,
                                    allowedPassengers=allowedPassengers, specialInfo=specialInfo)
            user.isDriver = True
            user.save()
            request.session['is_driver'] = True

            driver.save()
            # TODO 修改为driver 页面
            return redirect('/Driver/')

    driver_register_form = DriverRigisterForm()
    #TODO figure out the use of this part of code
    # driver_name = request.session['user_name']
    # driver = models.User.objects.get(username=driver_name)
    # driver_info_Num = driver.driverinfo_set.count()
    # driver_info = driver.driverinfo_set.all()
    return render(request, "login/driverRegister.html", locals())


def index(request):
    if request.method == "GET" and request.GET:
        if 'Driver' in request.GET:
            if request.session.get('is_driver', None):
                return redirect('/Driver/')
            else:
                return redirect('/driverRegister/')
        else:
            return redirect('/passenger/')

    return render(request,'login/index.html')

def login(request):
    # if already logged in redirect
    if request.session.get('is_login', None):
        return redirect("/index/")

    if request.method == "POST":
        login_form = UserForm(request.POST)
        message = "please check the content！"
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            try:
                user = models.User.objects.get(name=username)
                if user.password == password:
                    request.session['is_login'] = True
                    request.session['user_id'] = user.id
                    request.session['user_name'] = user.name
                    #判断是否为driver
                    request.session['is_driver'] = user.isDriver
                    return redirect('/index/')
                else:
                    message = "password incorrect！"
            except:
                message = "user does not exist！"
        return render(request, 'login/login.html', locals())
    else:
        login_form = UserForm()
        return render(request, 'login/login.html', locals())

def register(request):
    if request.session.get('is_login', None):
        # if already signed in, then cannot register
        return redirect("/index/")
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        message = "Please check the content！"
        if register_form.is_valid():  # get the detaile data
            username = register_form.cleaned_data['username']
            password1 = register_form.cleaned_data['password1']
            password2 = register_form.cleaned_data['password2']
            email = register_form.cleaned_data['email']
            if password1 != password2:  # pass word are not the same
                message = "The passwords are not the same！"
                return render(request, 'login/register.html', locals())
            else:
                same_name_user = models.User.objects.filter(name=username)
                if same_name_user:  # found the same user name
                    message = 'user already exists！'
                    return render(request, 'login/register.html', locals())
                same_email_user = models.User.objects.filter(email=email)
                if same_email_user:  #  found the same email
                    message = 'email already exits！'
                    return render(request, 'login/register.html', locals())

                # all rules passed

                new_user = models.User.objects.create()
                new_user.name = username
                new_user.password = password1
                new_user.email = email
                new_user.save()
                return redirect('/login/')  # return to login page
    register_form = RegisterForm()
    return render(request, 'login/register.html', locals())

# log out in login page
def logout(request):
    if not request.session.get('is_login', None):
        # 如果本来就未登录，也就没有登出一说
        return redirect('/login/')
    request.session.flush()
    # 或者使用下面的方法
    # del request.session['is_login']
    # del request.session['user_id']
    # del request.session['user_name']
    # return redirect("/index/")
    return redirect('/login/')