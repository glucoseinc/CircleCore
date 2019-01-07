.PHONY: build
build:
	docker build -t circle-core .
	docker tag circle-core:latest circle-core:$(shell git rev-parse --short HEAD)
