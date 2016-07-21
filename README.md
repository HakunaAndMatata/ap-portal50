# CS50 AP Portal

## Instructions for running portal50 on C9

* Create a new Django workspace on Cloud9
  * Under "Clone from Git", paste in git@github.com:brianyu28/ap-portal50.git
* Once in the workspace, run
  * `python manage.py runserver $IP:$PORT`
  * A popup will appear on the top right of your terminal with link to the application
* To log in and view Portal features, use
  * username = davey
  * password = davey

## Dependencies

(incomplete list)

* mysql-python

## Features

Settings 

* Can change color of your custom curriculum (requested by teachers to make school colors)
* Can set location so that header of curriculum will be "This is CS50 <location>."

Customize

* Can toggle entire chapters, modules, and individual resources on and off
* Click either "Your Site" on sidebar or "View Your Curriculum" to see changes
* On an individual module page, teachers can add notes which will appear above the resources
* Teacher's site can be viewed by anyone, even if not logged in, via /username/

Resources

* Can sort all of the resources in the wiki by type, and search all the resources