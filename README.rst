Content Inspection Proxy
========================

Status: Beta

A proxy, a gate to your system
In fact a highly configurable and extensible proxy on top on your api

Use cases
 * throttling
 * content inspection


testing
-------
unittests:
`python cip/test.py`


integraiton tests:
`DEBUG=1 python cip/func_tests.py`


TODO
----

allow for xsd to be also passed through (downloadable)
allow for wsdl pass through when overwriting remote host name
