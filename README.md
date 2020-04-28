## Fake CKAN harvest source

Use this repo to create your own WAF harvest source.

### Setup

Create your [virtual environment](https://virtualenvwrapper.readthedocs.io/en/latest/)

`mkvirtualenv fake-ckan_harvest_source`

Install dependencies

`pip install -r requirements.txt`

### Running the fake harvest source server

`python main.py`

### Testing the server

WAF page will default the url index to 0 but otherwise will be dependant on the number provided in the url


Navigate to `http://localhost:8001/1/` to see WAF index 1, `http://localhost:8001/2/` to see WAF index 2, etc up to 10

Navigate to `http://localhost:8001/1/num_links-50/` to define the number of links up to 99.

    http://localhost:8001/1/num_links-20/ will generate 20 links, omitting the num_links will generate 10 links

Navigate to `http://localhost:8001/1/num_links-50/delay-5/` to define the delay on the server.

    http://localhost:8001/1/num_links-20/delay-5/ will delay the server by 5 seconds, omitting the delay will delay the processing by 1 second

The url index generates a uniquely repeatable guid so that the harvest source will be harvested.

### Targeting the harvest source from a [docker-ckan](https://github.com/alphagov/docker-ckan) stack

In order to target the fake harvest source use this URL - http://docker.for.mac.localhost:8001/<index number 0 - 99>/
