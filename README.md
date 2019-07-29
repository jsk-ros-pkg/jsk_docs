# jsk_docs

[![Build Status](https://travis-ci.org/jsk-ros-pkg/jsk_docs.svg?branch=master)](https://travis-ci.org/jsk-ros-pkg/jsk_docs)
[![Documentation Status](https://readthedocs.org/projects/jsk-docs/badge/?version=latest)](http://jsk-docs.readthedocs.org/en/latest/?badge=latest)

Document is available on [readthedocs.org](http://jsk-docs.readthedocs.org/en/latest/?badge=latest).


## How to add repository?

Add repository to the `subproject` of the `jsk_docs`. See https://readthedocs.org/dashboard/jsk-docs/subprojects/ for mor detail.


## How to generate doc on local environment?

```bash
cd doc
source ./setup.sh
make html
make auto  # and go to http://127.0.0.1:8888
```
