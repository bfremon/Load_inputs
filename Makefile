rm = rm -fr
py = /usr/bin/python3

deb: setup.py clean
	$(py) setup.py --command-packages=stdeb.command \
	bdist_deb


.PHONY: clean

clean:
	$(rm) *.tar.gz *.egg-info dist/ deb_dist/
