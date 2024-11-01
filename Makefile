SHELL = /bin/bash
define USAGE=
@echo -e
@echo -e "Usage:"
@echo -e "\tmake run [arg=sync]                         -- run script"
@echo -e "\tmake black [arg=--<arg>]                    -- format python with black"
@echo -e "\tmake flake                                  -- run flake8"
@echo -e
endef

# Argument passed from commandline, optional for some rules, mandatory for others.
arg =


.PHONY: run
run:
	python3 ./sodar_check/run.py

.PHONY: black
black:
	black . -l 80 --skip-string-normalization --exclude ".git|.venv|env|src|" $(arg)

.PHONY: flake
flake:
	flake8 .


.PHONY: usage
usage:
	$(USAGE)
