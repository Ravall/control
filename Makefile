CONTROL_DIR=.

integrate: pylint-strict-real pep8-strict tests

git-update:
	git pull origin master
	git submodule update --init

update: git-update

params:
	@echo "PROJECT=control\nTAG=0" > project.params


PYLINT=	pylint
PYLINT_OPTIONS=-rn -d 'R0801,R0904,R0903,C0111,C0302,C0304,W0142,W0141,F0401,W0108,W0232,W0105,I' \
	--generated-members=filter,id,relation_name

tests:
	. /home/envs/sancta/bin/activate; python -m unittest discover


pylint-strict-real:
	. /home/envs/sancta/bin/activate; $(PYLINT) -f parseable --ignore=migrations $(PYLINT_OPTIONS) dj

rm_pyc:
	find . -name '*.pyc' -delete

pep8-strict:
	. /home/envs/sancta/bin/activate; pep8 --ignore=E501 $(STRICT_STYLE_FILES)

STRICT_STYLE_FILES=\
	dj \
	fab \
	deploy
