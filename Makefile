.PHONY: help docker-build docker-test docker-demo test clean

IMAGE_NAME ?= asymmetric-engine

help:
	@echo "Available commands:"
	@echo "  make docker-build - Build Docker container image"
	@echo "  make docker-test  - Build and run unit tests inside Docker container"
	@echo "  make docker-demo  - Run end-to-end pipeline demo inside Docker container"
	@echo "  make test         - Run unit tests locally using pytest"
	@echo "  make clean        - Clean temporary files, caches, and build artifacts"

docker-build:
	docker build -t $(IMAGE_NAME) -f engine/Dockerfile .

docker-test: docker-build
	docker run --rm $(IMAGE_NAME)

docker-demo: docker-build
	docker run --rm $(IMAGE_NAME) python3 examples/pipeline_demo.py

test:
	pytest -v tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type f -name "*.py[cod]" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
