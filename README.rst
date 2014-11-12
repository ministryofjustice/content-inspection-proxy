Content Inspection Proxy
========================
Status: Beta

A fully configurable and extensible proxy on top on your api

Use cases
 * throttling
 * latency simulation
 * content inspection


Building
--------
Before you start please install Docker on your environment.
In case of OSX please follow `Docker Install <https://docs.docker.com/installation/mac/>`_.
It's also recommended to install `fig <http://www.fig.sh/>`_.


To build docker image::

    docker build -t cip .


To build & run pvb integration environment::

    # clone pvb frontend
    # clone content-inspection-proxy
    # clone domis-server
    cd ../prison-visits
    fig up


To build local python dev environment::

    # On OSX follow Python install guide (https://gist.github.com/munhitsu/1034876)
    # build virtualenv
    mkvirtualenv cip
    # install requirements
    pip install -r requirements.txt


testing
-------
unittests::

    # you will need to run all content inspection components somewhere
    # one way is to login to your docker image (docker run -i -t cip /bin/bash)
    # other is to use local python dev environment
    python cip/test.py


pvb integration tests::

    # make sure your fig based integration environment runs
    # make sure you have python environment ready
    DEBUG=1 python cip/func_tests.py


TODO
----

1. On SOAP Allow for xsd to be also passed through (downloadable)
2. On SOAP Allow for wsdl pass through when overwriting remote host name
3. Separate content-inspection-proxy code from pvb specific configuration
