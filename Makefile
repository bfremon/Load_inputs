rm = rm -fr
py = /usr/bin/python3
cp = /bin/cp

deb: setup.py
	$(py) setup.py --command-packages=stdeb.command \
	bdist_deb
	@echo '==> Copying built deb files to '$(PWD)'/'
	$(cp) deb_dist/*.deb .

whl: setup.py
	$(py) setup.py bdist_wheel
	@echo '==> Copying built whl files to '$(PWD)'/'
	$(cp) dist/*.whl .

.PHONY: clean

clean:
	$(rm) *.tar.gz *.egg-info dist/ deb_dist/ \
	*.deb *.whl venv/
