# Create your views here.
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from time_engine.models import TimeTable
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from datetime import date
from json import dumps

from django.views.decorators.csrf import csrf_exempt

# User registration

def register(request):
    if request.method == "POST":
        User.objects.create_user(request.POST['username'], None, request.POST['password'])
    return render(request, 'time_engine/register.html')


#in settings add: settings.LOGIN_URL ='login'
#@login_required
def login(request):
    if request.method == "POST":
        user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])

        if user is not None:
            #the password verified for the user
            if user.is_active:
                print("User is valid, active and authenticated")
                return redirect("index")
            else:
                print("The password is valid, but the account has been disabled!")

        else:
            print("The username and password were incorrect.")
    return render(request, 'time_engine/login.html')


# Each view is it's own function.
# Each view takes at least one arg: HttpRequest object
# Each view must return a HttpResponse object
# the HttpResponse object takes a string parameter which is the content
# of the page we're sending to the client requesting the view


# TO USE THE USER MODEL FROM DJANGO:
# IN VIEWS inside of POST handling code
# from django.contrib.auth.models import User
#
# item = YourModel()
# item.user = User.objects.all()[0]


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    if request.method == "POST":
        # User is saving / updating a timetable
        print "POST method called"
        return HttpResponse("post was called")

    else:

        # Construct a dictionary to pass to the template engine as its context.
        # Note the key boldmessage is the same as {{ boldmessage }} in the template!
        timetable_list = TimeTable.objects.all()
        context_dict = {'alltimetables': timetable_list}

        # Return a rendered response to send to the client.
        # We make use of the shortcut function to make our lives easier.
        # Note that the first parameter is the template we wish to use.
        return render_to_response('time_engine/index.html', context_dict, context)
        #return HttpResponse("Hello World! You're at the Time Engine Index! Woot!")

@csrf_exempt
def ajax(request):
    if request.method == "POST":
        timetable = TimeTable()
        user = User()
        user.username = request.POST["user"]
        user.save()
        timetable.user = user
        timetable.start_date = date.today()
        timetable.name = request.POST["name"]
        timetable.lesson_count = request.POST["lesson_count"]
        timetable.save()

    timetable_list = list(TimeTable.objects.all())
    ajax_list = []
    for thing in timetable_list:
        ajax_list.append({
            "name": thing.name,
            "user": str(thing.user),
            "creation_date": str(thing.creation_date),
            "lesson_count": thing.lesson_count,
        })
    return HttpResponse(dumps(ajax_list, indent=4), content_type="application/json")

def dom(request):
    if request.method == "POST":
        print request.POST
    return render(request, 'time_engine/dom.html')

def jsexample(request):
     return render(request, 'time_engine/jsexample.html')

# a simple view that doesn't involve any data being passed along
# for example an about page
# def dom(request):
#    return render(request, 'time_engine/dom.html')

def options(request):
    return HttpResponse("This is the Preferences page.")

def engine(request):
    return HttpResponse("This is the Engine!")

def results(request):
    return HttpResponse("This is the results page.")

def date_looping(request):
    return render(request, 'time_engine/date_looping.html')
