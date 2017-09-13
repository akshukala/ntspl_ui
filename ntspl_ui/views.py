from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
import requests
import json
from django.contrib.auth.decorators import (
    login_required, user_passes_test
)
from django.conf import settings
from django.contrib.auth.views import login as login_view

def process_user_service_token(request):
    '''
    Request processor for setting Candidate service token. Will only work with
    a django login request.
    '''
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        url = settings.USER_SERVICE_URL + "uservalidation/"

        payload = {
            "mobileNo": username,
            "password": password
        }

        headers = {'content-type': 'application/json'}
        # TODO: Inspect the certificate issue and set verify to True
        r = requests.post(url, data=json.dumps(payload), headers=headers,
                          verify=False)
        #if username/password is correct then only below condition is satisfied
        print r.content
        if r.status_code == 200 and not "errorCode" in json.loads(r.content):
        	
            key = 'session'
            value = r.cookies[key]
            request.session['userservice_key'] = value
        else:
        	return HttpResponseRedirect("/")

@login_required(login_url="/login/")        	
def index(request):
	return render_to_response("index.html",locals(),RequestContext(request))

def ntspl_login(request, *args, **kwargs):
    response = login_view(request, *args, **kwargs)
    process_user_service_token(request)
    return response

@login_required(login_url="/login/")
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
