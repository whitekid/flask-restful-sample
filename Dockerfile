FROM python:2-onbuild

EXPOSE 5000

CMD python manage.py runserver -h 0.0.0.0
