# Gulis

## Installation
	pip install gulis
or

	git clone git@github.com:maxis1718/gulis.git
	cd gulis
	python setup.py install
	
	
## Development

use mkvirtualenv

	mkvirtualenv gulis
	workon gulis

install required packages

	pip install -r requirements.txt
	python gulis/crawl.py


## Testing

install nose and coverage globally

	sudo pip install nose
	sudo pip install coverage

run tests with coverage

	nosetests --with-coverage --cover-package=gulis
