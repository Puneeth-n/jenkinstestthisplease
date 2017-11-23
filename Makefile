#!/usr/bin/env make

build:
	@docker build -f ./Dockerfile -t puneethn/jenkinstestthisplease .

develop:
	@docker run --rm -it -v $(PWD):/opt/ct -w /opt/ct -p 8000:80 puneethn/jenkinstestthisplease:latest bash

pull:
	@docker pull puneethn/jenkinstestthisplease:latest

start: pull
	@docker run --rm -p 8000:80 puneethn/jenkinstestthisplease:latest

exec:
	@docker run --rm -it puneethn/jenkinstestthisplease:latest bash

install:
	@pip install -r requirements.txt

.PHONY: develop
