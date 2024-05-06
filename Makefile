rm = rm -fr
py = /usr/bin/python3
cp = /bin/cp
sudo = /usr/bin/sudo  
apt = $(sudo) /usr/bin/apt-get install
venv_path = $(PWD)/venv
vpy = $(venv_path)/bin/python3
vpip = $(venv_path)/bin/pip3

debs_packages = 

pre: requirements.txt
	$(apt) dh-python python3-stdeb $(debs_packages)
	$(vpip) install -r requirements.txt

deb: setup.py pyproject.toml
	$(py) setup.py --command-packages=stdeb.command \
	bdist_deb
	@echo '==> Copying built deb files to '$(PWD)'/'
	$(cp) deb_dist/*.deb .

whl: setup.py pyproject.toml
	$(py) setup.py bdist_wheel
	@echo '==> Copying built whl files to '$(PWD)'/'
	$(cp) dist/*.whl .

test:
	$(py) -m unittest discover

.PHONY: clean

clean:
	$(rm) *.tar.gz *.egg-info dist/ deb_dist/ \
	*.deb *.whl venv/
