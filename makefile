run:
	py boot.py

setup-win:
	py -m pip install -r requirements-win.txt

setup-mac:
	py -m pip install -r requirements-mac.txt

fmt:
	py -m autopep8 -r -i -a -a --ignore=E402,E721 .

.PHONY: bumpup
bumpup:
	py tools\bumpup.py
.PHONY: build
build:
	py tools\build.py
