.PHONY: install
.PHONY: depends
.PHONY: lint
.PHONY: test

# This makefile contains a whole bunch of shortcuts and scripted
# Things that are convenient to not have to remember

install:
	#python setup.py build
	#sudo python setup.py install

depends:
	# TODO - consider using pip rather than apt-get
	sudo apt-get install python-pygame python-nose pep8

lint:
	pep8 .

test:
	nose .
