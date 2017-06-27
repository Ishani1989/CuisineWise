# Cuisine Wise app

Cuisine Wise is an application built in Python that lists a variety of cuisines and dishes associated with each cuisine. Users can browse through their favorite cuisines and view their corresponding recipes.
This project uses Google's single sign on feature to allow users to login and add/update/delete information. The project.py file when run, starts a server on port 5000 and displays the latest 5 dishes added to our database on the home page.

![alt text](https://github.com/Ishani1989/CuisineWise/blob/master/static/screenshots/HomePage.JPG "Home Page for Cuisine Wise app")

Click on cuisine on the left to view specific dishes

![alt text](https://github.com/Ishani1989/CuisineWise/blob/master/static/screenshots/CuisineSpecificDishes.JPG "Cuisine Specific Dishes")

Click on particular dish to view its description

![alt text](https://github.com/Ishani1989/CuisineWise/blob/master/static/screenshots/DishDescriptionPage.JPG "Dish Description")

## Dependency

Python version 2.7.13<br />
Flask version 0.12.2<br />
Jinja2 version 2.9.6<br />
SQLite3 version 2.6.0<br />
SQLAlchemy version 1.1.10<br />
HTML 5<br />
Javascript version 1.7<br />
Bootstrap version 3.3.7<br />
jQuery version 3.2.1<br />

## External API Dependency

Google Sign In API<br />

## How to run

First, we need to create a database to hold our tables. Run the database_setup.py file to create a database for our project.
We can add data manually, but for a quick solution, we can run addDataToCuisine.py file to fill our tables with some dummy data.
Next, we need to create a project in the Google developers console and substitute the client Id and project id with the ones we just created. 
Download the Json file for the client id and name it client_secrets.json and keep it in the same folder as your project.py file.
Run the project.py file to start the server at port 5000. We can view the app by visiting localhost:5000 from our browser.

## Tested Env

Tested in Chrome version 57.0.2987.133

## History

First checkin done on June 25, 2017

## Credits

ishanibhattacharjee@gmail.com<br />
https://stackoverflow.com<br />
https://udacity.com<br />
http://flask.pocoo.org/docs/0.12/<br />