**This is just a list of commands I've found useful for project maintenance**


* Update README.rst

    ```pandoc -s -t rst --toc README.md -o README.rst```

* Install project with files.txt record

    ```sudo python setup.py install --record files.txt```

* "uninstall" package installed with files.txt record

    ```cat files.txt | sudo xargs rm -rf```

* Generate/update base docs/ folder with Sphinx

    ```sphinx-apidoc -F -o docs shissen```

* Run tests from root project directory

    * `py.test --cov="shissen" --cov-report=term --cov-report=html`
    * `nosetests --with-cov --cov-report term-missing --cov shissen tests/`
    * With `tox>=1.8.0` installed for py27
