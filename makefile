SHELL := /bin/bash

install:
	python3.9 -m venv venv; \
	source venv/bin/activate; \
	pip3 install --upgrade pip; \
	pip3 install -r requirements.txt; \

run:
	source venv/bin/activate; \
	cd src; \
	python3 business_card.py; \
