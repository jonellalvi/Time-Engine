from datetime import date
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from json import dumps
from django.core import serializers

from calc_eventlist import EventList
from time_engine.forms import TimeTableForm, UserForm, UserProfileForm
from time_engine.models import TimeTable, Result

from django.shortcuts import render_to_response
from django.contrib import auth
from django.shortcuts import redirect
from utilities import getGravatarImage

# Each view is it's own function.
# Each view takes at least one arg: HttpRequest object
# Each view must return a HttpResponse object
# The HttpResponse object takes a string parameter which is the content
# of the page we're sending to the client requesting the view



# User registration
# This is based on http://www.tangowithdjango.com/book17/chapters/login.html
@csrf_exempt
def register(request):

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == "POST":

        # Get form fields
        try:
            email = request.POST['username']
            password = request.POST['password']
        except KeyError:
            # Invalid form data
            return HttpResponseBadRequest('Malformed form')

        # Look up user
        try:
            User.objects.get(username=email)
        except ObjectDoesNotExist:
            # Create new user with this name & password
            User.objects.create_user(email, email, password)
            return HttpResponse(dumps({'result': True}), content_type="application/json")
        else:
            print "User already exists"
            return HttpResponse(dumps({'result': False, 'msg': 'User already exists'}), content_type="application/json")

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        #profile_form = UserProfileForm()


# User login
# This is based on http://www.tangowithdjango.com/book17/chapters/login.html
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == "POST":
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # USe Django's machinery to attempt to see if the username/password
        # combo is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                login(request, user)
                # Then send the user back to the homepage.
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


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details, for example.
    context = RequestContext(request)

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

            # extract the cleaned data from the form
            form_data = form.cleaned_data

            # Create the EventList object
            eventlist = EventList(form_data)
            # Get the list of events
            result = eventlist.get_eventlist()
            print "this is result: ", result

            # get the event time:
            event_time = form_data['start_time']
            print "this is the event_time: ", event_time

            # get the last date from the event list:
            last_item = result[-1]
            print "This is the LAST DATE datetime: ", last_item

            # now format it as a string:
            end_date = last_item.strftime("%A %B %d, %Y")
            end_date_label = "End Date:"
            print "This is the LAST DATE formated", end_date, type(end_date)

            # now format the datetimes to send to full Calendar
            # and package up to send
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
            event_color = form_data['color']
            options = 'color: ' + form_data['color']
            print "these are the options: ", options

            # package it up to send:
            cal_data = {'cal_events': {'events': events, 'color': event_color},
                        'end_event': {'end_date_label': end_date_label, 'end_date': end_date}
            }

            # extract the save boolean set in the js to see if we need to save.
            save_option = form.cleaned_data['save']
            # if it's save, save to database
            print "the user is: ", request.user
            if save_option == "true":
                timetable_id = save_timetable(form_data, request.user, result)
                response = {'cal': cal_data, 'form': request.POST, 'id': timetable_id}
            else:
                response = {'cal': cal_data, 'form': request.POST}
            print "This is cal_data", cal_data

            #response = {'cal': cal_data, 'form': request.POST, 'id': timetable_id}
            return HttpResponse(dumps(response), content_type="application/json")
        else:
            return HttpResponse('{"status": "invalid form!"}', content_type="application/json")

    else:
        # if you're logged in, get a list of the saved timetables for that user
        # get the username request.user
        # then use that to look up the saved
        if request.user.is_authenticated():
            timetable_list = TimeTable.objects.filter(user_id=request.user.id)
            timetable_list = list(timetable_list)
            timetable_list.append(TimeTable())
        else:
            timetable_list = []
        #
        # # I think this is where we delete it if they want to?
        # if request.POST.get('delete'):
        #     print "HERE IS WHERE THE TIMETABLE IS DELETED"


        form = TimeTableForm()
        return render(request, 'time_engine/index.html', {'timetables': timetable_list})


def save_timetable(form_data, user, eventlist):
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
    tt.end_date = eventlist[-1]
    tt.user = user
    tt.save()

    for idx, event in enumerate(eventlist):
        result = Result()
        result.lesson_date = event
        result.lesson_num = idx + 1
        result.timetable = tt
        result.save()

    return tt.id


# get timetable view
@login_required
@csrf_exempt
def get_timetable(request):

    # Get the timetable's id from the request data:
    ttid  = request.GET['id']
    print "This is ttid: ", ttid

    # use the timetable's id to return the list of dates
    # from the Results model:
    eventlist = Result.objects.filter(timetable_id=ttid)

    # use the timetable's id to return the color
    # from the TimeTable model:
    eventcolor = TimeTable.objects.get(id=ttid).color
    print "this is what I get for eventcolor:", eventcolor

    # get  end date from TimeTable
    eventend = TimeTable.objects.get(id=ttid).end_date
    print "this is eventend: ", eventend

    # now package it up to send back:
    elist = serializers.serialize("json", eventlist)
    data = {'elist': elist, 'eventcolor': eventcolor, 'eventend': str(eventend)}

    #return HttpResponse(serializers.serialize("json", eventlist), content_type="application/json")
    return HttpResponse(dumps(data), content_type="application/json")


# only delete if logged in
@login_required
@csrf_exempt
def delete_timetable(request):
    # Get the timetable's id from the request data:
    ttid  = request.POST['id']

    # use the timetable's id to return the timetable:
    deltt = TimeTable.objects.filter(pk=ttid)

    # now axe that baby:
    huh = deltt.delete()

    #TODO: implement a soft delete with a new column in the model "enabled" and
    #TODO: to true by default, and set to false if deleted
    #TODO: then check in the template and display based on enabled...
    # for now just return a success message:

    msg = "timetable deleted!"
    print msg

    return HttpResponse(dumps({'msg': msg, 'ttid': ttid}), content_type="application/json")



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



def options(request):
    return HttpResponse("This is the Preferences page.")


