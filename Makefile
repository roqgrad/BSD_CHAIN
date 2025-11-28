# Makefile for FreeBSD Custom OS Builder

.PHONY: help all clone customize build iso clean test

PYTHON := python3
BUILDER := $(PYTHON) freebsd_builder.py
CONFIG := example_config.json

help:
	@echo "FreeBSD Custom OS Builder - Makefile"
	@echo ""
	@echo "Usage:"
	@echo "  make all          - Run complete workflow"
	@echo "  make clone        - Clone FreeBSD source"
	@echo "  make customize    - Apply customizations"
	@echo "  make build        - Build the OS"
	@echo "  make iso          - Create ISO image"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make test         - Run tests"
	@echo ""
	@echo "Configuration:"
	@echo "  CONFIG=$(CONFIG)"

all:
	$(BUILDER) --all --config $(CONFIG)

clone:
	$(BUILDER) --clone --config $(CONFIG)

customize:
	$(BUILDER) --customize --config $(CONFIG)

build:
	$(BUILDER) --build --config $(CONFIG)

iso:
	$(BUILDER) --create-iso --config $(CONFIG)

clean:
	$(BUILDER) --clean --config $(CONFIG)

test:
	$(PYTHON) -m pytest tests/ -v

setup-ports:
	$(BUILDER) --setup-ports --config $(CONFIG)

build-packages:
	$(BUILDER) --build-packages --config $(CONFIG)

release:
	$(BUILDER) --build-release --config $(CONFIG)

memstick:
	$(BUILDER) --create-memstick --config $(CONFIG)
