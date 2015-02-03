# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.shortcuts import render
from time_engine.models import TimeTable
from django.contrib.auth.models import User
from django.contrib import auth
from django.shortcuts import redirect
from datetime import date
from json import dumps
from time_engine.forms import TimeTableForm, UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from calc_eventlist import EventList


from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
#from .forms import TimeTableForm

# Each view is it's own function.
# Each view takes at least one arg: HttpRequest object
# Each view must return a HttpResponse object
# the HttpResponse object takes a string parameter which is the content
# of the page we're sending to the client requesting the view


# User registration
# This is based on http://www.tangowithdjango.com/book17/chapters/login.html
def register(request):
    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False
    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":
        # Attempt to grab info from the raw from information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        # This was the old one:
        #User.objects.create_user(request.POST['username'], None, request.POST['password'])

        # if the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            #Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context
    return render(request,
                  'time_engine/register.html',
                  {'user_form': user_form, 'profile_form': profile_form, 'registered': registered})


# User login
# This is based on http://www.tangowithdjango.com/book17/chapters/login.html
def user_login(request):

    #If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # USe Django's machinery to attempt to see if the username/password
        # combo is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If Non (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # WE'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/time_engine/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Time Engine account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'time_engine/login.html', {})


# Logout
# Use the login_required() decorator to ensure only those logged in can access the view
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/time_engine/')



#in settings add: settings.LOGIN_URL ='login'
#@login_required
# def login(request):
#     if request.method == "POST":
#         user = auth.authenticate(username=request.POST['username'], password=request.POST['password'])
#
#         if user is not None:
#             #the password verified for the user
#             if user.is_active:
#                 print("User is valid, active and authenticated")
#                 return redirect("index")
#             else:
#                 print("The password is valid, but the account has been disabled!")
#
#         else:
#             print("The username and password were incorrect.")
#     return render(request, 'time_engine/login.html')



def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

    # This is for ModelForms:
    # form = TimeTableForm()

    # if this is a POST request we need to process the form data:
    # this is an ajax request:
    if request.method == "POST":
        print request.POST['name']
        # User is saving / updating a timetable
        print "POST method called"
        # create a form instance and populate it with data from the request:
        # This is called binding the data to the form
        form = TimeTableForm(request.POST)

        # check if it's vaild:
        if form.is_valid():
            #process the data in form.cleaned_data as required
            # IS THIS WHERE THE CALCULATION WOULD GO FOR MY TIMETABLE?
            # See example at https://docs.djangoproject.com/en/1.7/topics/forms/
            name = form.cleaned_data['name']
            color = form.cleaned_data['color']
            start_date = form.cleaned_data['start_date']
            start_time = form.cleaned_data['start_time']
            event_count = form.cleaned_data['event_count']
            has_saturday = form.cleaned_data['has_saturday']
            has_monday = form.cleaned_data['has_monday']
            has_tuesday = form.cleaned_data['has_tuesday']
            has_wednesday = form.cleaned_data['has_wednesday']
            has_thursday = form.cleaned_data['has_thursday']
            has_friday = form.cleaned_data['has_friday']
            has_sunday = form.cleaned_data['has_sunday']
            save_option = form.cleaned_data['save']
            form_data = form.cleaned_data
            print "this is form_data: ", form_data
            # https://docs.djangoproject.com/en/1.7/ref/forms/api/#accessing-clean-data
            # now I have a dictionary of the values.
            # here's a sample of what form.cleaned_data returns:
            # {
            #   'has_thursday': False,
            #   'name': u'Spam',
            #   'color': u'yellow',
            #   'start_time': datetime.time(4, 20),
            #   'has_tuesday': False,
            #   'has_saturday': False,
            #   'has_wednesday': True,
            #   'lesson_count': 14,
            #   'has_monday': True,
            #   'has_friday': True,
            #   'start_date': datetime.date(2000, 3, 25)
            # }
            eventlist = EventList(form_data)
            result = eventlist.get_eventlist()
            print "this is result: ", result

            event_time = form_data['start_time']

            print "this is the event_time: ", event_time


            events = []

            for i, r in enumerate(result):
                evt = {'title': 'event: ' + str(i + 1),
                       'start': r.isoformat() + 'T' + str(event_time),
                       'allDay': False
                }
                print r
                events.append(evt)

            #now append the options:
            # color:
            print "the color is: ", form_data['color']
            event_color = form_data['color']
            options = 'color: ' + form_data['color']
            print "these are the options: ", options
            #events_with_options = events + options
            #print "This is events which go to the calendar: ", events

            print "these are the events with options: ", events

            # format a dictionary that looks like test_events but with my data:
            test_events = { 'events': [
                {
                    'title':  'event1',
                    'start': '2015-01-09T12:30:00',
                    'allDay': False
                },
                {
                    'title'  : 'woot2',
                   'start'  : '2015-01-10T12:30:00',
                    'allDay' : False
                },
                {
                    'title'  : 'event3',
                   'start' : '2015-01-11T12:30:00',
                    'allDay' : False
                }
            ]
            # color: 'black',     # an option!
            # textColor: 'yellow' # an option!
             }

            # if it's save, save to database
            if save_option == "true":
                timetable_id = save_timetable(form_data, request.user)


            date_strings = test_events#[dt.strftime("%A %B %d, %Y") for dt in result]
            #print date_strings
            # now format the data to be passed to FullCalendar
            #return HttpResponseRedirect("")
            return HttpResponse(dumps({'events': events, 'color': event_color}), content_type="application/json")
        else:
            return HttpResponse('{"status": "invalid form!"}', content_type="application/json")


    else:
        form = TimeTableForm()
    return render(request, 'time_engine/index.html', {'form': form})

    # else:
    #
    #     # Construct a dictionary to pass to the template engine as its context.
    #     # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    #     timetable_list = TimeTable.objects.all()
    #     context_dict = {
    #         'alltimetables': timetable_list,
    #         #The following is for modelForms:
    #         #'form': form
    #     }
    #
    #     # Return a rendered response to send to the client.
    #     # We make use of the shortcut function to make our lives easier.
    #     # Note that the first parameter is the template we wish to use.
    #     return render_to_response('time_engine/index.html', context_dict, context)
    #     #return HttpResponse("Hello World! You're at the Time Engine Index! Woot!")

# only save if logged in.
def save_timetable(form_data, user):
    # take form_data and massage it and save to model.
    print "save to model !!!", form_data
    tt = TimeTable()
    tt.name = form_data['name']
    tt.color = form_data['color']
    tt.start_date = form_data['start_date']
    tt.start_time = form_data['start_time']
    tt.event_count = form_data['event_count']
    tt.has_saturday = form_data['has_saturday']
    tt.has_monday = form_data['has_monday']
    tt.has_tuesday = form_data['has_tuesday']
    tt.has_wednesday = form_data['has_wednesday']
    tt.has_thursday = form_data['has_thursday']
    tt.has_friday = form_data['has_friday']
    tt.has_sunday = form_data['has_sunday']
    tt.user = user
    tt.save()
    return tt.id

@csrf_exempt
def ajax(request):
    if request.method == "POST":
        timetable = TimeTable()
        user = User.objects.all()[0]
        #user.username = request.POST["user"]
        #user.save()
        timetable.user = user
        timetable.start_date = date.today()
        timetable.start_time = date.today().time()
        timetable.name = request.POST["name"]
        #timetable.lesson_count = request.POST["lesson_count"]
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

# View for basic form:

