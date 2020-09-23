# CourseCollocationPlatform
A web  based platform that solves the problems faced by elearners of any age 

## User behaviour tracking technique 
Simple Machine Coding </br>
Self Made Algorithm based project </br>



## IDEA: 
To track the user activity on the portal of what courses user is searching and recording 
the details on a non sql mongodb database and when the user logs out the data is processed by a algorithm 
summarize the search results.
Then the search results are stored in a cookie in the browser.
when the user logins again the cookie is searched and the data of cookie is used to show some favourable 
results to user.

==================================================================================================================

### STEPS AND FLOW OF SEQUENCE AMONG PAGES:


1.From the index.html page user can signup or login if already has an account.</br>
  On first login genral results will be shown to user.

2.When the user logs in *index() function in views.py*  page runs and creates a session and stores the user email in session.(Later on this email will be used to identify         coresponding mongo db collection for user) </br>
  Then user is redirected to *courses.html* page where courses are displayed.

3.When the *courses.html* page loads *userlogin() function* from *views.py* runs and calls the *scarper2() function in views.py* is called it does the job of _WEBSCRAPING_ of the course details from websites. </br>
(webscraping details)

~ *beautifullsoup4 library* of python has been used for web scarping
~ After the html content is fetched by webscraping an object *of scraper class from forms.py* is created.
~ *Scraper class* contains empty lists in which each detail likr *e.g(course_title,duration,rating,author,level)* is stored and .object is returned to *userlogin function*
~ Then a *zipped list of all lists of scraped data* is sent with http request which loads courses page. </br>

 _When the *courses.html* page runs there is *for loop* that initializes iterator for each list of details of courses
   then creates html syntax form to display the course details containing a submit button inside the form with class (course_record)_

4. When ever the user clicks on a course the submit button runs and javascript event handler runs on *courses.html page*
   It prevents default reload behaviour and calls an AJAX FUNCTION() containg this info:
 
   '(type:"GET" , url:"/record/", data: title,rating,link,level  is sent with ajax)'

   This calls the [tracker_storage() function in views.py page] this function:
		~ creates a connection with the mongo db database </br>
		~ takes the data sent with ajax request and apeends in the specific collection for user
		  having lists for each different detail. </br>
		~ this storing happens for each click on the courses on the webpage(courses.html) </br>

5. When the user clicks on logout button on the courses.html page javascript runs the url logout
   and then the *logout() function from views.py page is run* this does following steps.
	~ creates connection with mongodb collection for the user. </br>
	~ runs the algorithm to process all the lists stored in the collection </br>
	~ summarizes the data of collection </br>
	~ then stores the summarized data in COOKIE named"btitle"  in the browser </br>
	~ when the user will login again this cookie will be searched and will used to provide user speacific results for the user.
