# CourseCollocationPlatform
A web  based platform that solves the problems faced by elearners of any age 


IDEA: to track the user activity on the portal of what courses user is searching and recording 
the details on a non sql mongodb database and when the user logsout the data is processed by a algorithm 
summarize the search results .then the search results are stored in a cookie in the browser.
when the user logins again the cookie is searched and the data of cookie is used to show some favourable 
results to user.
==================================================================================================================

STEPS AND FLOW OF SEQUENCE AMONG PAGES::
----------------------------------------

1. from the index.html page user can signup or login if already has an account.
	on first login genral results will be shown to user.

2.when the user logs in [index() function in views.py ] page runs and creates a session and stores the 
	user email in session.(later on this email will be used to identify coressponding mongo db collection for user)
	then user is redirected to (courses.html)  page where courses are displayed.

3.when the courses.html page loads [userlogin()] function from views.py runs and calls the 
	(scarper2() function in views.py) is called it does the job of
	WEBSCRAPING of the course details from websites.(webscraping details)
		-beautifullsoup4 library of python has been used for web scarping
		-after the html content is fetched by webscraping an object (of scarper class from forms.py)
		  is created it contains empty lists in which each detail,e.g(course_title,duration,rating,author,level)
		   is stotred .obeject is returned to userlogin function then an {zipped list of all lists of scraped data}
		   is sent with http request which loads courses page. 

	|when the corses.html  page runs there is for loop that intializes iterator for each list of details of courses
		then creates html syntax  form to display the course details .containing a submit button inside the form
 		with class (course_record).

4. when ever the user clicks on a course the submit button runs and javascript event handler runs (on courses.html page)
 it prevents default reload behaviour and calls a AJAX FUNCTION() containg this info::
(type:"GET" , url:"/record/", data: title,rating,link,level  is sent with ajax)

-this calls the [tracker_storage() function in views.py page] this function:
		|-creates a connection with the mongo db database
		|-takes the data sent with ajax request and apeends in the specific collection for user
			having lists for each different detail.
		|-this storing happens for each click on the courses on the webpage(courses.html)

5.when the user clicks on logout button on the courses.html page javascript runs the url logout
and then the (logout() function from views.py page is run) this does following steps.
	|-creates connection with mongodb collection for the user.
	|-runs the algorithm to process all the lists stored in the collection
	|-summarizes the data of collection
	|-then stores the summarized data in COOKIE named"btitle"  in the browser
	|-when the user will login again this cookie will be searched and will used to provide user speacific
	 results for the user.
