# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.shortcuts import render
from . import forms
from . import models

from pymongo import MongoClient
from googleproject.models import user

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

# Create your views here.
# def test():
# return render('signup.html')
def get_site_file(url):
    try:
        html = urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')  # for converting to html
        return bs

    except HTTPError as e:
        print(e)

def search(request):
    object = forms.scraper()
    # passing output string to object of scraper class in forms.py
    search=request.GET['search_word']

    page_cousera = get_site_file("https://www.coursera.org/search?configure%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BruleContexts%5D%5B0%5D=en&indices%5Bprod_all_products_term_optimization%5D%5Bpage%5D=1&query="+str(search))
    if page_cousera == None:
        print('The file could not be found coursera')
    else:
        courses = page_cousera.find_all('li', {'class': 'ais-InfiniteHits-item'})  # html tag li
        for course in courses:  # for traversing whole list of courses
            try:
                course_title = course.h2.get_text()
                course_image = course.find('img', {'alt': str(course_title)}).get('src',None)  # .find for finding from inspect elemet and .get for getting url
                course_link = "https://www.coursera.org" + course.find('a', {
                    'class': 'rc-MobileSearchCard'}).get('href', None)
                course_duration = course.find('span', {'class': 'partner-name'}).get_text()
                course_detail = course.find('span', {'class': 'partner-name'}).get_text()
                course_rating = course.find('span', {'class': 'ratings-text'}).get_text()
                course_level = course.find('span', {'class': 'difficulty'}).get_text()
                object.Title.append(f"{course_title}")
                object.Detail.append(f"{course_detail}")
                object.link.append(f"{course_link}")
                object.image.append(f"{course_image}")
                object.duration.append(f"{course_duration}")
                object.rating.append(f"{course_rating}")
                object.level.append(f"{course_level}")
                print("akash akash akash")
                list = zip(object.Title, object.Detail, object.link, object.image, object.duration, object.rating,
                           object.level)  # as multiple list so we have to zip
                return render(request, 'googleproject/courses.html', {'test_result': list})
            except AttributeError as e:
                print(str(e)+"dont do this")
                return render(request,'googleproject/index.html')





def index(request):
    form = forms.search_form()
    if request.method == 'POST':
        form = forms.search_form(request.POST)
        if form.is_valid():
              # input form index page
            # rating=form.cleaned_data['rating']#input from index page
            if request.session.get("id"):
                print(request.session["id"] + "if of index")
                objectb = scraper2(request)    # consist of details of all object from scraper 2 fn
                list = zip(objectb.Title, objectb.Detail, objectb.link, objectb.image, objectb.duration, objectb.rating,
                           objectb.level)   # as multiple list so we have to zip
                return render(request, 'googleproject/courses.html', {'test_result': list})   #it will return to courses.html
            else:
                objectb = scraper2(request) #it returns webscraping object
                print("normal index else")

                list = zip(objectb.Title, objectb.Detail, objectb.link, objectb.image, objectb.duration, objectb.rating,
                           objectb.level)
                return render(request, 'googleproject/courses.html', {'test_result': list})  # object returned to page

    return render(request, 'googleproject/index.html',
                  {'forms': form})  # if no input is there empty website than form is generated returned to page


def user_login(request):
    print("user loggs")
    if request.session.get("id"):
        print("user returning by session")
        email=request.session["email"]
        object = scraper2(request)
        list = zip(object.Title, object.Detail, object.link, object.image, object.duration, object.rating,
                   object.level)

        return render(request,'googleproject/courses.html', {'test_result': list, 'message': email})

    if request.method == 'POST':
        print("from login page")
        if request.POST['email']:
            email = request.POST['email']
            password = request.POST['password']
            con = MongoClient("mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
            db = con.get_database('user')
            collection = db.user_tracking

            try:
                poll = collection.find({"email": email, "password": password})
                time = datetime.datetime.now()
                request.session.set_expiry(100000*36)
                request.session["email"] = email
                request.session["id"] = email + str(time)
                if request.session.get("id"):
                    print(request.session["id"])

                    object = scraper2(request)
                    list = zip(object.Title, object.Detail, object.link, object.image, object.duration, object.rating,
                               object.level)

                    return render(request,'googleproject/courses.html', {'test_result': list, 'message': email})
                else:
                    return render(request, 'googleproject/user_login.html',
                                  {'error_message': "technical error try again after some time session"})
            except Exception as e:
                return render(request, 'googleproject/user_login.html',
                              {'error_message': "username or password is wrong"+str(e)})
    else:
        print("user_login function else")
        return render(request, 'googleproject/user_login.html')

    # serach result page  for future use after prototype
    # if run throught changing url by adding 'searchshow/' to url as seen in urls.py


def tracker_storage(request):
    print("tracker storage"+request.GET["atitle"])
    try:
        conn = MongoClient("mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
        db = conn.get_database('user')
        collection = db.user_tracking
        print(request.GET["atitle"])
        collection.update_one(
            {"email": request.session["email"]},
            {"$set": {"test": request.GET["atitle"]},    #for changing data
             "$push": {"title": request.GET["atitle"], "level": request.GET["alevel"],
                       "rating": request.GET["arating"]}}
        )
        cursor = collection.find()
        for record in cursor:
            print(record)
    except Exception as e:
        print(e.__str__())    #for printing error
    return render(request, "googleproject/index.html")


def logout(request):
    print("logout")
    con = MongoClient("mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
    db = con.get_database('user')
    collection = db.user_tracking
    email = request.session["email"]
    response = render(request,"googleproject/index.html")         #returning to logout page as session end
    poll = collection.find({"email": email}, {"title": 1, "level": 1, "rating": 1, "_id": 0})
    title=""
    for p in poll:
        maxcount = 0
        for t in p["title"]:
            temp = p["title"].count(t)
            if maxcount < temp:
                maxcount = temp
                print("title" + str(maxcount))
                title=t

    response.set_cookie('Course_Collocation_akas', str(title), path='/',max_age=3600*24*10000) # cookie for 100 days
    print(email)
    collection.update_one(    #emptied list so that for next session new list could be created
        {"email": email},
        {"$set": {"test": title, "title": [], "level": [], "rating": []}}
    )
    request.session.flush()
    return response


def scraper2(request):
    import random
    object = forms.scraper()  # passing output string to object of scraper class in forms.py
    if request.COOKIES.get("btitle"):    #btitle from logout fn in views.py as it is just fetching cookies n comes froom browser
        print('cookie scrape')
        search = request.COOKIES['btitle']    #gives search string
        search=search.replace(" ","+")         # as url dont have space so converted to + sign
    else:
        print('noncookie scrape')
        search = ["courses","big%data","artificial%intelligence","french","python","c++","c","web%development","speaking"]
    j = random.randint(0, 8)
    print(search[j])

    for i in range(4):
        page_cousera = get_site_file(
            "https://www.coursera.org/search?query=" + search[j] + "&indices%5Bprod_all_products_term_optimization%5D%5Bpage%5D=" + str(
                i) + "&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BruleContexts%5D%5B0%5D=en&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true")
        #str(i) for accessing different courses # search is for cookies variable
        # coursera scraping
        if page_cousera == None:
            print('The file could not be found coursera')
        else:
            courses = page_cousera.find_all('li', {'class': 'ais-InfiniteHits-item'})   #html tag li
            for course in courses:   # for traversing whole list of courses
                try:
                    course_title = course.h2.get_text()
                    course_image = course.find('img', {'class': 'product-photo'}).get('src', None)    #.find for finding from inspect elemet and .get for getting url
                    course_link = "https://www.coursera.org" + course.find('a', {
                        'class': 'rc-DesktopSearchCard anchor-wrapper'}).get('href', None)
                    course_duration = course.find('span', {'class': 'partner-name'}).get_text()
                    course_detail = course.find('span', {'class': 'partner-name'}).get_text()
                    course_rating = course.find('span', {'class': 'ratings-text'}).get_text()
                    course_level = course.find('span', {'class': 'difficulty'}).get_text()
                    # session storage

                    # session storage ends
                    object.Title.append(f"{course_title}")
                    object.Detail.append(f"{course_detail}")
                    object.link.append(f"{course_link}")
                    object.image.append(f"{course_image}")
                    object.duration.append(f"{course_duration}")
                    object.rating.append(f"{course_rating}")
                    object.level.append(f"{course_level}")
                except AttributeError as e:
                    print(e)

        # craper code ends here
        # print(request.session["title"])

    return object  # object returned to page (returns to index function)


def user_signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        mobile1 = request.POST['mobile1']
        confirmpassword = request.POST['confirmpassword']
        if password != confirmpassword:
            return render(request, 'googleproject/signup.html',
                          {'message': "password and confirm password should be same"})
        else:
            print("passworfd is correct")
            try:
                #mongodb+srv://akash:<password>@cluster0.5pec5.mongodb.net/<dbname>?retryWrites=true&w=majority
                conn = MongoClient(
                    "mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
                print("connected sucessfully")
                db = conn.get_database('user')
                collection = db.user_tracking
                rec1 = {
                    "email": email,
                    "password":password,
                    "mobile":mobile1,
                    "title": [],
                    "level": [],
                    "rating": []
                }
                rec1_id = collection.insert_one(rec1)
                # print("id is:" + rec1_id)d
                user.objects.create(email=email, password=password, mobile=mobile1, user_type="general",
                                    tracking_id=rec1_id)
                cursor = collection.find()

                for record in cursor:
                    print(record)
            except Exception as e:
                print(e.__str__())
            request.session.flush()
            return render(request, 'googleproject/user_login.html', {'message': "welcome our new user"})
    else:
        return render(request, 'googleproject/signup.html')
