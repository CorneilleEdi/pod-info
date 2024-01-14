IMAGE := pod-info
VERSION := 2.0.0

.PHONY: build
build:
	docker build -t ghcr.io/corneilleedi/${IMAGE}:${VERSION} -f ./app/Dockerfile ./app

.PHONY: push
push:
	docker push ghcr.io/corneilleedi/${IMAGE}:${VERSION}

