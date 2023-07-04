.PHONY: clean pip-compile-dev pip-compile update-env run-app clean activate-env init isort black flake8 lint lang-create-po-folders lang-update lang-generate-pot lang-update-po lang-generate-mo

#################################################################################
# GLOBALS                                                                       #
#################################################################################

SHELL=/bin/bash

PROJECT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
PROFILE = default
PROJECT_NAME = circular-city-index-viewer
PACKAGE_NAME = circular-city-index-viewer
ENV_NAME = circular-city-index-viewer
SRC_CODE_FOLDER = app
SRC_CODE_PATH = ./${SRC_CODE_FOLDER}
PYTHON_INTERPRETER = python
PORT = 8889

# multi-language
LANGS = ca es en nl
LOCALES_PATH = ./locales
PO_FILES = $(wildcard ${LOCALES_PATH}/*/LC_MESSAGES/base.po)
MO_FILES = $(PO_FILES:.po=.mo)

XGETTEXT = xgettext
MSGMERGE = msgmerge

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## activate venv
activate-venv:
	source activate $(ENV_NAME)

## init development tools
init: activate-venv
	$(PYTHON_INTERPRETER) -m pip install pip-tools

## run app
run-app: activate-env
	streamlit run app/streamlit_app.py --server.port $(PORT)

## Delete all compiled Python files
clean: lang-clean
	find . -name "*.py[co]" -exec rm {} \;

## generate requirements-dev.txt
pip-compile-dev: requirements-dev.in activate-venv
	pip-compile requirements-dev.in

## generate requirements.txt
pip-compile: requirements.in activate-venv
	pip-compile requirements.in

## update environment
update-env: pip-compile-dev pip-compile activate-venv
	pip-sync requirements.txt requirements-dev.txt

# ref: https://github.com/j4ckp0t85/enigma2/blob/ef25da0da6d51cb8ea87361ee49892fdfefbb097/po/Makefile.am
## lang create folders and templates
lang-create-po-folders:
	for lang in $(LANGS); \
	do \
		mkdir -p ${LOCALES_PATH}/$$lang/LC_MESSAGES; \
		cp -n ${LOCALES_PATH}/base.pot ${LOCALES_PATH}/$$lang/LC_MESSAGES/base.po; \
		sed --in-place ${LOCALES_PATH}/$$lang/LC_MESSAGES/base.po --expression="s/Language\: \\\n/Language\: $$lang\\\n/"; \
	\
	done

## Update multi-language (pot and po) files
lang-update: lang-generate-pot lang-update-po

## Regenerate base.pot with new translations
lang-generate-pot:
	mkdir -p ${LOCALES_PATH}; \
	find ${SRC_CODE_PATH} -type f -iname "*.py" | xargs \
	$(XGETTEXT) \
		--from-code=UTF-8 \
		--language=Python \
		--add-comments="TRANSLATORS:" \
		--no-wrap \
		--sort-by-file \
		--output-dir ${LOCALES_PATH} \
		--output base.pot; \
	sed -i 's/charset=CHARSET/charset=UTF-8/g' ${LOCALES_PATH}/base.pot

## Update .po files with new translations from base.pot
lang-update-po::
	for po in ${LOCALES_PATH}/*/*/*.po; \
	do \
		$(MSGMERGE) \
			--no-wrap \
			--no-fuzzy-matching \
			--sort-by-file \
			--output-file $$po.new \
			$$po \
			${LOCALES_PATH}/base.pot \
			&& \
		mv $$po.new $$po; \
	\
	done

.PHONY:
$(MO_FILES): %.mo : %.po
	msgfmt $< -o $@

## lang: Generate mo files
lang-generate-mo: $(MO_FILES)

## clean language files
lang-clean:
	rm -f $(MO_FILES)

## sort imports
isort:
	isort .

## prettify code with black
black:
	black .

## run the flake8 tool
flake8:
	flake8 .

## linter
lint: flake8 isort black

## bump version
bump-version: activate-env
	cz bump --changelog


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := show-help

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
