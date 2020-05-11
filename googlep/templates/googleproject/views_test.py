# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from . import forms
from . import models


# Create your views here.
def test():
    return render('signup.html')


def index(request, flag=0):

    form = forms.search_form()
    if request.method == 'POST' or  flag==1:
        print("new requset")
        form = forms.search_form(request.POST)
        if form.is_valid():
            search = form.cleaned_data['search2lower']  # input form index page
            # rating=form.cleaned_data['rating']#input from index page
            flag=1
            if request.session.get("id"):
                print(request.session["id"] + "if of index AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
                cour=my_paging(request)
                print(cour)
                return render(request, 'googleproject/courses.html', {'object_list': cour})  # object returned to page
            else:
                cour = my_paging(request)
                print(cour)
                return render(request, 'googleproject/courses.html', {'object_list': cour})  # object returned to page

    return render(request, 'googleproject/index.html',
                  {'forms': form})  # if no input is there empty website than form is generated returned to page


def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "akashoct204@gmail.com" and password == "akash":
            time = datetime.datetime.now()
            request.session.set_expiry(300)
            request.session["id"] = email + str(time)
            request.session['search'] = []
            request.session['button'] = []

            if request.session.get("id"):
                print(request.session["id"])
                cour=my_paging(request)
                return render(request, 'googleproject/courses.html', {'object_list': cour, 'message': email})
            else:
                return render(request, 'googleproject/user_login.html',
                              {'error_message': "technical error try again after some time session"})
        else:
            return render(request, 'googleproject/user_login.html', {'error_message': "username or password is wrong"})
    else:
        return render(request, 'googleproject/user_login.html')
    # serach result page  for future use after prototype
    # if run throught changing url by adding 'searchshow/' to url as seen in urls.py


#paging function
def my_paging(request):
    print("paaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaging")
    object = scraper2(request)

    # /paging starts herr
    #  try :
    page = request.GET.get('page', 1)
    # except ValueError:
    #   page=1

    paginator = Paginator(object, 12)
    try:
        courses = paginator.page(page)
    except PageNotAnInteger:
        courses = paginator.page(1)
    except EmptyPage:
        courses = paginator.page(paginator.num_pages)
    # paging ends here
    return courses

def scraper2(request):
    LIST=[]     # list of objects
    # scraper code starts here
    from urllib.request import urlopen
    from urllib.error import HTTPError
    from bs4 import BeautifulSoup
    def get_site_file(url):
        """
        url - base url to access desired web file
        """
        try:
            html = urlopen(url)
            bs = BeautifulSoup(html, 'html.parser')
            return bs

        except HTTPError as e:
            print(e)

    search = request.GET.get('search', "course")
    # page_content = get_site_file('https://www.coursera.org/search?query=data%20science&')
    for i in range(2):
        page_cousera = get_site_file(
            "https://www.coursera.org/search?query=" + search + "&indices%5Bprod_all_products_term_optimization%5D%5Bpage%5D=" + str(
                i) + "&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BruleContexts%5D%5B0%5D=en&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true")
        # coursera scraping
        if page_cousera == None:
            print('The file could not be found coursera')
        else:
            objectss=[]
            courses = page_cousera.find_all('li', {'class': 'ais-InfiniteHits-item'})
            for i in courses:
                objectss.append(forms.scraper())    # passing output string to object of scraper class in forms.py

            zipp=zip(objectss,courses)
            for object,course in zipp:
                try:
                    course_title = course.h2.get_text()
                    course_image = course.find('img', {'class': 'product-photo'}).get('src', None)
                    course_link = "https://www.coursera.org" + course.find('a', {
                        'class': 'rc-DesktopSearchCard anchor-wrapper'}).get('href', None)
                    course_duration = course.find('span', {'class': 'partner-name'}).get_text()
                    course_detail = course.find('span', {'class': 'partner-name'}).get_text()
                    course_rating = course.find('span', {'class': 'ratings-text'}).get_text()
                    course_level = course.find('span', {'class': 'difficulty'}).get_text()
                    # session storage
                    '''request.session["title"].append(course_title)
                    request.session["link"].append(course_link)
                    request.session["rating"].append(course_rating)
                    request.session["level"].append(course_level)'''

                    object.Title=f"\t {course_title}"
                    object.Detail=f" \t {course_detail}"
                    object.link=f"\t {course_link}"
                    object.image=f"\t{course_image}"
                    object.duration=f"\t{course_duration}"
                    object.rating=f"\t{course_rating}"
                    object.level=f"\t{course_level}"
                    LIST.append(object)
                except AttributeError as e:
                    print(e)

        # craper code ends here
        # print(request.session["title"])

    return LIST  # object returned to page


def course(request):
    if request.method == 'GET':
        if request.session.get('id'):
            request.session['search'].append(request.GET['search'])
            request.session['button'].append(request.GERT['buttons'])
