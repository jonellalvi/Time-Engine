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
from django.template.loader import render_to_string
from django.db import connection
from django.views.decorators.http import require_http_methods

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

# csrf = cross site request forgery
@csrf_exempt
@require_http_methods(["POST"])
def register(request):

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


# User login
# This is based on http://www.tangowithdjango.com/book17/chapters/login.html
def user_login(request):

    if request.method == "POST":
        # Gather the username and password from the sign in form
        username = request.POST['username']
        password = request.POST['password']

        # Check if the username/password combo is valid
        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, log the user in.
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
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        # TODO: fix to send to modal instead of template
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
    # context = RequestContext(request)

    # if this is a POST request we need to process the timetable form data:
    # this is an ajax request:
    if request.method == "POST":
        # sanity checks:
        print request.POST['name']
        # User is saving / updating a timetable
        print "POST method called"
        # create a form instance and populate it with data from the request.
        # This is called binding the data to the form
        form = TimeTableForm(request.POST)

        # check if it's valid:
        if form.is_valid():

            # extract the cleaned data from the form
            form_data = form.cleaned_data

            # Create the EventList object
            # This class is called from the calc_eventlist module
            # EventList takes the data from the form as a parameter.
            eventlist = EventList(form_data)

            # Use the eventlist instance to get the list of events
            # using the get_eventlist method within EventList
            result = eventlist.get_eventlist()

            # get the event time
            event_time = form_data['start_time']

            # get the last date from the event list:
            last_item = result[-1]

            # now format it as a string
            # so it can be displayed
            end_date = last_item.strftime("%A %B %d, %Y")
            # also create a label to pass back to the form
            # for when we update it with the end date.
            end_date_label = "End Date:"

            # now format the datetimes to send to full Calendar
            # and package up to send
            # create a new empty list
            events = []

            # Create a list that formats each event so it
            # can be displayed in Full Calendar
            for i, r in enumerate(result):
                evt = {'title': 'event: ' + str(i + 1),
                       'start': r.isoformat() + 'T' + str(event_time),
                       'allDay': False
                       }

                # append the event to the events list:
                events.append(evt)

            # now append the options:
            # color:
            event_color = form_data['color']
            # options = 'color: ' + form_data['color']

            # package it up to send:
            cal_data = {'cal_events': {'events': events, 'color': event_color},
                        'end_event': {'end_date_label': end_date_label, 'end_date': end_date}
                        }

            # extract the save boolean set in the javascript to see if we need to save.
            save_option = form.cleaned_data['save']

            # check if this is a new timetable or an existing one:
            if 'edit_id' in request.POST:
                tt_update_id = request.POST['edit_id']
            else:
                tt_update_id = None
            print "this is the tt update id: ", tt_update_id
            # then we're doing an edit
            # update the db with the new values (save)
            # pass back the new values to update the card.
            # pass a flag to save timetable to do an update instead.

            # if logged in, set save_option to true.
            if request.user.is_authenticated():
                save_option = "true"

            if save_option == "true":
                # if we're logged in then call save_timetable function to save
                timetable_id = save_timetable(form_data, request.user, result, tt_update_id)
                response = {'cal': cal_data, 'form': request.POST, 'id': timetable_id}
                # render the card and send it back.
                temptt = create_timetable(form_data, request.user, result)

                # temptt['id'] = timetable_id
                setattr(temptt, 'id', timetable_id)

                # add in ids for each event
                for e in cal_data['cal_events']['events']:
                    e['id'] = timetable_id

                ttcardhtml = render_to_string('time_engine/ttcard.html', {'timetable': temptt, 'checked': 'checked'})
                response['cardhtml'] = ttcardhtml
            else:
                response = {'cal': cal_data, 'form': request.POST, 'id': 0}




            # response = {'cal': cal_data, 'form': request.POST, 'id': timetable_id}

            return HttpResponse(dumps(response), content_type="application/json")
        else:
            return HttpResponse('{"status": "invalid form!"}', content_type="application/json")

    else:
        # if you're logged in, get a list of the saved timetables for that user
        # get the username request.user
        # then use that to look up the saved
        if request.user.is_authenticated():
            timetable_list = TimeTable.objects.filter(user_id=request.user.id)
        else:
            timetable_list = []

        return render(request, 'time_engine/index.html', {'timetables': timetable_list})



def create_timetable(form_data, user=None, eventlist=None):
    # take form_data and massage it and save to model.

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

    if eventlist:
        tt.end_date = eventlist[-1]

    if user:
        tt.user = user

    return tt


def save_timetable(form_data, user, eventlist, update_id):
    # take form_data and massage it and save to model.
    if not update_id:
        tt = create_timetable(form_data, user)
        tt.end_date = eventlist[-1]
        tt.save()
        print tt.end_date

        for idx, event in enumerate(eventlist):
            result = Result()
            result.lesson_date = event
            result.lesson_num = idx + 1
            result.timetable = tt
            result.save()
    else:
        # doing an update:
        tt = TimeTable.objects.get(id=update_id)
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
        tt.save()


        Result.objects.filter(timetable_id=update_id).delete()


        # cursor = connection.cursor()
        # cursor.execute("DELETE from time_engine_result WHERE id = %s", [update_id])


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
    ttid = request.GET['ttid']
    wantresults = 'op' in request.GET and request.GET['op'] == "results"



    # use the timetable's id to return the list of dates
    # from the Results model:
    #eventlist = Result.objects.filter(timetable_id=ttid)

    # use the timetable's id to return the color
    # from the TimeTable model:
    ttObj = TimeTable.objects.get(id=ttid)

    events = []
    if wantresults:

        eventlist = Result.objects.filter(timetable_id=ttid)
        #print "this is eventlist: ", eventlist
        for i, r in enumerate(eventlist):
            evt = {'title': 'event: ' + str(i + 1),
                   'start': r.lesson_date.isoformat() + 'T' + str(ttObj.start_time),
                   'allDay': False,
                   'id': ttid
            }
            #print r
            events.append(evt)

        #print "This is events: ", events

    # get  end date from TimeTable
    # temp_eventend = TimeTable.objects.get(id=ttid).end_date
    # print "this is tem_eventend: ", temp_eventend
    # eventend = temp_eventend.strftime("%A %B %d, %Y")
    # print "this is eventend: ", eventend

    # setattr(ttObj, 'eventend', eventend)

    # now package it up to send back:
    #elist = serializers.serialize("json", ttObj)
    #data = {'elist': elist}


    result_data = {
        "tt": {
            'pk': ttid,
            'color': ttObj.color,
            'end_date': ttObj.end_date.isoformat(),
            'event_count': ttObj.event_count,
            'has_friday': ttObj.has_friday,
            'has_monday': ttObj.has_monday,
            'has_tuesday': ttObj.has_tuesday,
            'has_wednesday': ttObj.has_wednesday,
            'has_thursday': ttObj.has_thursday,
            'has_saturday': ttObj.has_saturday,
            'has_sunday': ttObj.has_sunday,
            'name': ttObj.name,
            'start_date': ttObj.start_date.isoformat(),
            'start_time': ttObj.start_time.isoformat()
        },
        "result_dates": {
            'cal': {
                'cal_events': {
                    'events': events,
                    'color': ttObj.color,
                    'id': ttid
                }
            }
        }
    }

    #return HttpResponse(serializers.serialize("json", eventlist), content_type="application/json")
    # return HttpResponse(serializers.serialize("json", [ttObj]), content_type="application/json")
    return HttpResponse(dumps(result_data), content_type="application/json")





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


