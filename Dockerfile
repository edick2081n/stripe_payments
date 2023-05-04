FROM python:3.9
RUN mkdir app
RUN cd /app
WORKDIR /app


COPY . /app
RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
EXPOSE 8001
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
