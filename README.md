# movies-app
developed using django framework
to run project
python .\manage.py makemigrations .\movies_data
python .\manage.py sqlmigrate movies_data 0001
python .\manage.py migrate movies_data   
python manage.py migrate   
python .\manage.py runserver
go to http://localhost:8000/movies/ collect, store and display movie
go to http://localhost:8000/movies_list/ API
