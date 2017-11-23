#!/usr/bin/env make

build:
	@docker build -f ./Dockerfile -t jenkinstestthisplease .

develop:
	@docker run --rm -it -v $(PWD):/opt/ttp -w /opt/ttp -p 8000:80 jenkinstestthisplease:latest bash

pull:
	@docker pull puneethn/jenkinstestthisplease:latest

start: build
	@docker-compose up

exec:
	@docker run --rm -it jenkinstestthisplease:latest bash

install:
	@pip install -r requirements.txt

.PHONY: develop
