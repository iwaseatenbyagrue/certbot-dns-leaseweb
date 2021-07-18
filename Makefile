.PHONY: build clean image install publish test

DOCKER_IMAGE_NAME ?= certbot-dns-leaseweb
DOCKER_IMAGE_TAG ?= latest

build: clean
	python3 setup.py sdist bdist_wheel

image:
	docker build --rm --pull --tag $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_TAG) .

test:
	pip install .[test]
	tox -e lint
	tox

install :
	pip install .

clean:
	rm -rf build dist

publish : build
	python3 -m twine upload dist/* --ve
