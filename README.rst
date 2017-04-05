========
Overview
========

.. start-badges

.. list-table::
    :stub-columns: 1

    * - docs
      - |docs|
    * - tests
      - | |travis| |requires|
        | |coveralls| |codecov|
        | |landscape| |scrutinizer| |codacy| |codeclimate|
    * - package
      - |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/replotlib/badge/?style=flat
    :target: https://readthedocs.org/projects/replotlib
    :alt: Documentation Status

.. |travis| image:: https://travis-ci.org/benbaror/replotlib.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/benbaror/replotlib

.. |requires| image:: https://requires.io/github/benbaror/replotlib/requirements.svg?branch=master
    :alt: Requirements Status
    :target: https://requires.io/github/benbaror/replotlib/requirements/?branch=master

.. |coveralls| image:: https://coveralls.io/repos/benbaror/replotlib/badge.svg?branch=master&service=github
    :alt: Coverage Status
    :target: https://coveralls.io/r/benbaror/replotlib

.. |codecov| image:: https://codecov.io/github/benbaror/replotlib/coverage.svg?branch=master
    :alt: Coverage Status
    :target: https://codecov.io/github/benbaror/replotlib

.. |landscape| image:: https://landscape.io/github/benbaror/replotlib/master/landscape.svg?style=flat
    :target: https://landscape.io/github/benbaror/replotlib/master
    :alt: Code Quality Status

.. |codacy| image:: https://img.shields.io/codacy/REPLACE_WITH_PROJECT_ID.svg?style=flat
    :target: https://www.codacy.com/app/benbaror/replotlib
    :alt: Codacy Code Quality Status

.. |codeclimate| image:: https://codeclimate.com/github/benbaror/replotlib/badges/gpa.svg
   :target: https://codeclimate.com/github/benbaror/replotlib
   :alt: CodeClimate Quality Status

.. |version| image:: https://img.shields.io/pypi/v/replotlib.svg?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/replotlib

.. |downloads| image:: https://img.shields.io/pypi/dm/replotlib.svg?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/replotlib

.. |wheel| image:: https://img.shields.io/pypi/wheel/replotlib.svg?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/replotlib

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/replotlib.svg?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/replotlib

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/replotlib.svg?style=flat
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/replotlib

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/benbaror/replotlib/master.svg?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/benbaror/replotlib/


.. end-badges

Replotting matplotlib figure the css way

* Free software: BSD license

Installation
============

::

    pip install replotlib

Documentation
=============

https://replotlib.readthedocs.io/

Development
===========

To run the all tests run::

    tox

Note, to combine the coverage data from all the tox environments run:

.. list-table::
    :widths: 10 90
    :stub-columns: 1

    - - Windows
      - ::

            set PYTEST_ADDOPTS=--cov-append
            tox

    - - Other
      - ::

            PYTEST_ADDOPTS=--cov-append tox
