# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from urlparse import urlparse
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
import requests
from models import codes
from bs4 import BeautifulSoup


# Create your views here.
RUN_URL = u'https://api.hackerearth.com/v3/code/run/'
COMPILE_URL = u'https://api.hackerearth.com/v3/code/run/'
CLIENT_SECRET = '4dfd962b7931b9b7833159cf6a38dde05f88ef54'
permitted_languages = ["C", "CPP", "CSHARP", "CLOJURE", "CSS", "HASKELL", "JAVA", "JAVASCRIPT", "OBJECTIVEC", "PERL", "PHP", "PYTHON", "R", "RUBY", "RUST", "SCALA"]


AZURE_NLP = u'https://text-analytics-demo.azurewebsites.net/Demo/Analyze'
BING_SEARCH_API_KEY = '19d0dfef006d49bb9e167fcc66d1db77'

BING_URL = 'http://api.cognitive.microsoft.com/bing/v5.0/'

## Proxy declaration for KGP
http_proxy = "http://10.3.100.207:8080"
https_proxy = "http://10.3.100.207:8080"
def get_domain(url):
    """
    Given a url return its domain
    """
    parsed_uri = urlparse(url)
    return(parsed_uri.netloc)

def home(request):
    if request.user.is_authenticated():
        # if request.method == 'POST':
        #     # POST goes here . is_ajax is must to capture ajax requests.
        #     if request.is_ajax():
        #         lang = request.POST.get('lang')
        #         source = request.POST.get('source')
        #         inputl = request.POST.get('input')
        #         data = {"lang": lang, "source": source, "input": inputl}
        #         print (source)
        #         data = {
        #             'client_secret': CLIENT_SECRET,
        #             'async': 0,
        #             'source': source,
        #             'lang': lang,
        #             'input': inputl,
        #             'time_limit': 5,
        #             'memory_limit': 262144,
        #         }
        #
        #         # Post data to HackerEarth API
        #         s = requests.Session()
        #         s.mount("http://", requests.adapters.HTTPAdapter(max_retries=5))
        #         s.mount("https://", requests.adapters.HTTPAdapter(max_retries=5))
        #         r = s.post(RUN_URL, data=data)
        #         # extract important key words using azure api (of course I have done some smart things for it!)
        #         key_words = []
        #         compile_status = r.json()['compile_status'].strip()
        #         current_json = r.json()
        #         if compile_status != 'OK':
        #             nlp_req = s.get(AZURE_NLP, data={'inputText': str(compile_status)})
        #             content = BeautifulSoup(nlp_req.text, 'lxml')
        #             keywords_class = content.find_all('div', attrs={'class': 'row top-buffer'})[1]
        #             key_words = keywords_class.find_all('div')[1].find_all('mark')
        #             for idx in range(len(key_words)):
        #                 key_words[idx] = key_words[idx].text
        #
        #             key_words.append(compile_status)
        #             links = []
        #             desc = []
        #             import re
        #             for word in reversed(key_words):
        #                 page = s.get("https://www.google.co.in/search?q=" + word)
        #                 soup = BeautifulSoup(page.content, 'lxml')
        #                 links_ = soup.findAll("a")
        #                 for link in soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)")):
        #                     debug_url = link["href"].replace("/url?q=", "").split('&')[0]
        #                     if 'webcache.googleusercontent.com' in debug_url:
        #                         continue
        #                     links.append(debug_url)
        #                     desc_ = link.text
        #                     desc_ += ":" + get_domain(debug_url)
        #                     desc.append(desc_)
        #
        #             current_json['debug_urls'] = links[:10]
        #             current_json['descriptions'] = desc[:10]
        #         return JsonResponse(current_json, safe=False)
    # Get goes here
        return render(request, 'init.html')
    else:
        return render(request,'index.html')

@login_required
def codeplay(request):
    return render(request, 'codeplay.html')

@login_required
def profile(request):
    print request
    return render(request, 'profile.html')


def base(request):
    return render(request, 'base.html')


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})



"""
Check if source given with the request is empty
"""
def source_empty_check(source):
  if source == "":
    response = {
      "message" : "Source can't be empty!",
    }
    return JsonResponse(response, safe=False)


"""
Check if lang given with the request is valid one or not
"""
def lang_valid_check(lang):
  if lang not in permitted_languages:
    response = {
      "message" : "Invalid language - not supported!",
    }
    return JsonResponse(response, safe=False)


"""
Handle case when at least one of the keys (lang or source) is absent
"""
def missing_argument_error():
  response = {
    "message" : "ArgumentMissingError: insufficient arguments for compilation!",
  }
  return JsonResponse(response, safe=False)



"""
Method catering to AJAX call at /ide/compile/ endpoint,
makes call at HackerEarth's /compile/ endpoint and returns the compile result as a JsonResponse object
"""
def compileCode(request):
  if request.is_ajax():
    try:
      source = request.POST['source']
      # Handle Empty Source Case
      source_empty_check(source)

      lang = request.POST['lang']
      # Handle Invalid Language Case
      lang_valid_check(lang)

    except KeyError:
      # Handle case when at least one of the keys (lang or source) is absent
      missing_argument_error()

    else:
      compile_data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
      }

      r = requests.post(COMPILE_URL, data=compile_data)
      return JsonResponse(r.json(), safe=False)
  else:
    return HttpResponseForbidden();


"""
Method catering to AJAX call at /ide/run/ endpoint,
makes call at HackerEarth's /run/ endpoint and returns the run result as a JsonResponse object
"""
def runCode(request):
  if request.is_ajax():
    try:
      source = request.POST['source']
      # Handle Empty Source Case
      source_empty_check(source)

      lang = request.POST['lang']
      # Handle Invalid Language Case
      lang_valid_check(lang)

    except KeyError:
      # Handle case when at least one of the keys (lang or source) is absent
      missing_argument_error()

    else:
      # default value of 5 sec, if not set
      time_limit = request.POST.get('time_limit', 5)
      # default value of 262144KB (256MB), if not set
      memory_limit = request.POST.get('memory_limit', 262144)

      run_data = {
        'client_secret': CLIENT_SECRET,
        'async': 0,
        'source': source,
        'lang': lang,
        'time_limit': time_limit,
        'memory_limit': memory_limit,
      }

      # if input is present in the request
      code_input = ""
      if 'input' in request.POST:
        run_data['input'] = request.POST['input']
        code_input = run_data['input']

      """
      Make call to /run/ endpoint of HackerEarth API
      and save code and result in database
      """
      r = requests.post(RUN_URL, data=run_data)
      r = r.json()
      cs = ""
      rss = ""
      rst = ""
      rsm = ""
      rso = ""
      rsstdr = ""
      try:
        cs = r['compile_status']
      except:
        pass
      try:
        rss=r['run_status']['status']
      except:
        pass
      try:
        rst = r['run_status']['time_used']
      except:
        pass
      try:
        rsm = r['run_status']['memory_used']
      except:
        pass
      try:
        rso = r['run_status']['output_html']
      except:
        pass
      try:
        rsstdr = r['run_status']['stderr']
      except:
        pass

      code_response = codes.objects.create(
        username = request.user.username,
        code_id = r['code_id'],
        code_content = source,
        lang = lang,
        code_input = code_input,
        compile_status = cs,
        run_status_status = rss,
        run_status_time = rst,
        run_status_memory = rsm,
        run_status_output = rso,
        run_status_stderr = rsstdr
      )
      code_response.save()
      return JsonResponse(r, safe=False)
  else:
    return HttpResponseForbidden()


"""
View catering to /code_id=xyz/ URL
"""
def savedCodeView(request, code_id):
    try:
        result = codes.objects.get(code_id=code_id)
        code_content = result.code_content
        lang = result.lang
        code_input = result.code_input
        compile_status = str(result.compile_status.encode('utf-8')).decode('utf-8')
        run_status_status = result.run_status_status
        run_status_time = result.run_status_time
        run_status_memory = result.run_status_memory
        run_status_output = result.run_status_output
        run_status_stderr = result.run_status_stderr

        return render(request, 'init.html', {
            'code_content': code_content,
            'lang': lang,
            'inp': code_input,
            'compile_status': compile_status,
            'run_status_status': run_status_status,
            'run_status_time': run_status_time,
            'run_status_output': run_status_output,
            'run_status_memory': run_status_memory,
            'run_status_stderr': run_status_status
        })
    except codes.DoesNotExist:
        result = None
