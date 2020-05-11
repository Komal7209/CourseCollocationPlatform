# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render, render_to_response
from . import forms
from  . import models
import random
from pymongo import MongoClient
from googleproject.models import user
from django.template import RequestContext

# Create your views here.
#def test():
    #return render('signup.html')


def write():
    testing=models.course_track()
    testing.mTitle="stardom"


def index(request):
    form=forms.search_form()
    if request.method=='POST':
        form=forms.search_form(request.POST)
        if form.is_valid():
            search=form.cleaned_data['search2lower']#input form index page
            #rating=form.cleaned_data['rating']#input from index page
            if request.session.get("id"):
                print(request.session["id"]+"if of index")
                objectb = scraper2(request)
                list = zip(objectb.Title, objectb.Detail, objectb.link, objectb.image, objectb.duration, objectb.rating,
                           objectb.level)
                return render(request, 'googleproject/courses.html', {'test_result': list})
            else:
                objectb=scraper2(request)
                print("normal index else")

                list = zip(objectb.Title, objectb.Detail, objectb.link, objectb.image, objectb.duration, objectb.rating, objectb.level)
                return render(request, 'googleproject/courses.html', {'test_result': list})  # object returned to page

    return render(request,'googleproject/index.html',{'forms':form})#if no input is there empty website than form is generated returned to page

def user_login(request):
    print("here guy3")
    if request.method=='POST':
        print("here guy")
        if request.POST['email']:
            email=request.POST['email']
            password=request.POST['password']
            if user.objects.filter(email=email, password=password):
                time=datetime.datetime.now()
                request.session.set_expiry(300)
                request.session["id"]=email+str(time)
                if request.session.get("id"):
                    print(request.session["id"])
                    object=scraper2(request)
                    list = zip(object.Title, object.Detail, object.link, object.image, object.duration, object.rating,object.level)
                    response=render_to_response('googleproject/courses.html', {'test_result': list,'message': email})
                    response.set_cookie('id',email)
                    n=random.randint(1,6)
                    response.set_cookie('title',object.listt[n])
                    return response
                else:
                    return render(request, 'googleproject/user_login.html',{'error_message':"technical error try again after some time session"})
            else:
                return render(request, 'googleproject/user_login.html',{'error_message':"username or password is wrong"})
    else:
        print("user_login function else")
        return render (request, 'googleproject/user_login.html')


    #serach result page  for future use after prototype
    # if run throught changing url by adding 'searchshow/' to url as seen in urls.py

def tracker_storage(request):
    print("tiktpk")
    try:
        conn=MongoClient("mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
        print("connected sucessfully")
        db = conn.get_database('user')
        collection=db.user_tracking
        #email=request.session["email"]
        collection.update_one(
            {"email": "akashoct204@gmail.com"},
            {"$set": {"test": request.GET["atitle"]},
             "$push": {"title":request.GET["atitle"],"level":request.GET["alevel"],"rating":request.GET["arating"]}}
        )
        #request.session["storage_id"]=rec1_id
        #print("id is:"+str(rec1_id))
        cursor=collection.find()
        for record in cursor:
            print(record)
    except Exception as e:
        print(e.__str__())
    return render(request,"googleproject/index.html")

def logout(request):
    print("finsally")
    return render(request,"googleproject/index.html")


def scraper2(request):
    object = forms.scraper()  # passing output string to object of scraper class in forms.py
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
    #earch=request.GET.get('search',"course")
    if 'id' in request.COOKIES:
        print('cookie')
        search = request.COOKIES['title']
    else:
        print('noncookie')

        search = object.listt[0]
    print(search)
    # page_content = get_site_file('https://www.coursera.org/search?query=data%20science&')
    for i in range(3):
        page_cousera = get_site_file(
            "https://www.coursera.org/search?query="+search+"&indices%5Bprod_all_products_term_optimization%5D%5Bpage%5D=" + str(
                i) + "&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BclickAnalytics%5D=true&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BruleContexts%5D%5B0%5D=en&indices%5Bprod_all_products_term_optimization%5D%5Bconfigure%5D%5BhitsPerPage%5D=10&configure%5BclickAnalytics%5D=true")
        # coursera scraping
        if page_cousera == None:
            print('The file could not be found coursera')
        else:
            courses = page_cousera.find_all('li', {'class': 'ais-InfiniteHits-item'})
            for course in courses:
                try:
                    course_title = course.h2.get_text()
                    course_image = course.find('img', {'class': 'product-photo'}).get('src', None)
                    course_link = "https://www.coursera.org" + course.find('a', {
                        'class': 'rc-DesktopSearchCard anchor-wrapper'}).get('href', None)
                    course_duration = course.find('span', {'class': 'partner-name'}).get_text()
                    course_detail = course.find('span', {'class': 'partner-name'}).get_text()
                    course_rating = course.find('span', {'class': 'ratings-text'}).get_text()
                    course_level = course.find('span', {'class': 'difficulty'}).get_text()
                    #session storage

                    #session storage ends
                    object.Title.append(f"\t {course_title}")
                    object.Detail.append(f" \t {course_detail}")
                    object.link.append(f"\t {course_link}")
                    object.image.append(f"\t{course_image}")
                    object.duration.append(f"\t{course_duration}")
                    object.rating.append(f"\t{course_rating}")
                    object.level.append(f"\t{course_level}")
                except AttributeError as e:
                    print(e)

        # craper code ends here
        #print(request.session["title"])

    return object  # object returned to page

def user_signup(request):
    if request.method=='POST':
        email=request.POST['email']
        password=request.POST['password']
        mobile=request.POST['mobile']
        confirmpassword=request.POST['confirmpassword']
        if password!=confirmpassword:
            return render(request, 'googleproject/signup.html', {'message': "password and confirm password should be same"})
        else:
            print("passworfd is correct")
            try:
                conn = MongoClient(
                    "mongodb+srv://akash:akash@cluster0-5pec5.mongodb.net/test?retryWrites=true&w=majority")
                print("connected sucessfully")
                db = conn.get_database('user')
                collection = db.user_tracking
                rec1 = {
                    "email": email,
                    "title":[],
                    "level":[],
                    "rating":[]
                }
                rec1_id = collection.insert_one(rec1)
                #print("id is:" + rec1_id)
                user.objects.create(email=email, password=password, mobile=mobile,user_type="general", tracking_id=rec1_id)
                cursor = collection.find()
                for record in cursor:
                   print(record)
            except Exception as e:
                print(e.__str__())

            return render(request,'googleproject/user_login.html',{'message':"welcome our new user"})
    else:
        return render(request, 'googleproject/signup.html')