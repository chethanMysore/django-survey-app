# django-survey-app
This is a sample survey application built on [django-admin](https://github.com/django/django/tree/master/django/contrib/admin) following the [Django quick start tutorial](https://docs.djangoproject.com/en/3.1/intro/tutorial01/). This is a SPA built using django-framework where users can participate in surveys created by the administrator of the application. Each user participation is tracked by the administrator and is provided with visualizations on choice distributions for each question in the application. The administration dashboard is an extension of admin templates available in [django-admin](https://github.com/django/django/tree/master/django/contrib/admin). 

## Features:
 - The polls application is extended to a survey where admin can create multiple surveys with multiple questions and choices for each question.
 - The dashboard is enriched with a statistics widget. The widget displays the popular survey among the surveys and the bar chart visualization of vote distributions among different choices for a question.
 - The application is a SPA with 5 Views on the Users App and a dashboard for the administrator. Partial Views are implemented with a custom middleware view 'index' which further routes URL requests.
 - Created two REST endpoints and used them from admin through AJAX calls.
 
## Installation and Launching the application

### Requirements:

- python version > 3.6 installed
- django version > 3.1.5 installed

### Run
#### Check for possible schema changes while using the version control as well as for the first run. 
Navigate to the project directory (where manage.py is located) and run
  ```cmd
  python manage.py makemigrations survey
  ```
#### Create schema for models incorporated in survey app. (The sql script returned can be used shared across teams)
  ```cmd
  python manage.py sqlmigrate survey 0001
  ```
#### Commit  all changes to the databases. This also creates necessary tables in the database.
  ```cmd
  python manage.py migrate
  ```
#### Collect all static assets and add to build/root folder in main application scope
  ```cmd
  python manage.py collectstatic
  ```
#### Create an admin user for the application
  ```cmd
  python manage.py createsuperuser
  ```
#### Run the development server
  ```cmd
  python manage.py runserver
  ```
  
- Suggestion: Run this with sudo(linux) and as administrator in windows so that the changes reflect at real time.
- After running the above command, the survey application will be available at http://localhost:8000/survey and the admin portal can be accessed at http://localhost:8000/admin


## Resources Used
 - [django](https://www.djangoproject.com/)
 - [nested-admin](https://github.com/django/django/tree/master/django/contrib/admin)
 - python
 - [JQuery](https://jquery.com/)
 - [chart.js](https://www.chartjs.org/)
 
## Additional files added and overrided templates from django-admin
 - <b>static/*</b>: the folder consists of static assets used by the application like JS, CSS, Images. <b>static/JS</b> also includes a custom Javascript file, [survey_admin.js](https://github.com/chethanMysore/django-survey-app/blob/master/static/js/survey-admin.js). the file contains logic to create charts and make AJAX calls to get nested survey entities. <b>static/CSS</b> includes [survey-app.css](https://github.com/chethanMysore/django-survey-app/blob/master/static/css/survey-app.css) and [survey-stats.css](https://github.com/chethanMysore/django-survey-app/blob/master/static/css/survey-stats.css) to include custom css for widgets and changing overview of the admin portal.
 - <b>templates/admin/*</b>: the folder consists of overrided templates created as a copy from django-admin. This includes [admin/base.html](https://github.com/chethanMysore/django-survey-app/blob/master/templates/admin/base.html), [admin/base_site.html](https://github.com/chethanMysore/django-survey-app/blob/master/templates/admin/base_site.html) and [admin/index.html](https://github.com/chethanMysore/django-survey-app/blob/master/templates/admin/index.html).
 
## Results:
### About Page
Gives a brief description of the goals and features of the application




