============
uData-gouvfr
============

.. image:: https://secure.travis-ci.org/etalab/udata-gouvfr.png
    :target: http://travis-ci.org/etalab/udata-gouvfr
    :alt: Build status
.. image:: https://coveralls.io/repos/etalab/udata-gouvfr/badge.png?branch=master
    :target: https://coveralls.io/r/etalab/udata-gouvfr
    :alt: Code coverage

uData customizations for Etalab / Data.gouv.fr.

Compatibility
=============

udata-gouvfr requires Python 2.7+ and uData.


Installation
============

You can install udata-gouvfr with pip:

.. code-block:: console

    $ pip install udata-gouvfr

or with easy_install:

.. code-block:: console

    $ easy_install udata-gouvfr


Development
===========

To use it within your udata local instance, follow these steps:

.. code-block:: console

    $ pip install requirements.txt

Put udata_gouvfr and udata_harvest within your PYTHON_PATH
and then alter your udata settings.py file with these values:

    PLUGINS = ['gouvfr', 'harvest']
    THEME = 'gouvfr'
