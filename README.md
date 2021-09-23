Setup
-----

Install scrapy
````
pip install virtualenv
virtualenv -p python3 env
source env/bin/activate
pip install scrapy
````

Get the SPIDer
````
git clone https://github.com/peppelinux/SPIDer.git
````

Run
````
cd SPIDer/spid
scrapy crawl -L INFO spid.gov.it
````

Developers
----------

start a project, then inherit the SPIDer in your spider class

````
scrapy startproject spid
cd spid
scrapy genspider links www.spid.gov.it
````
