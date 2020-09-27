# CourseCollocationPlatform
A web  based platform that solves the problems faced by elearners of any age. 
Platform was made to  provide personalized recommendation of courses to the user.

1. details of courses are collected by WEBSCRAPING from several websites and are shown to user.

2. When user searches a keyword or opens any course through AJAX request a function is called which stores that action
  in MONGO DB ATLAS by accessing the document of given user by its userid.
  
3. when user logsout a python file is run which iterates all data stored in mongo db document then stores summary of
  that session by processing it and storing it in a COOKIE on user browser.
  
4. when user logs in again that cookie is searched and its data is used to give recommendation of courses to the user.
