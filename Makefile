NAME = $(shell basename $(CURDIR))
VERSION = latest

run:
	python manage.py runserver

test:
	python sample/tests.py

docker-build:
	docker build -t $(NAME):$(VERSION) .

docker-run: docker-build
	docker run -d -p 5000:5000 $(NAME):$(VERSION)
