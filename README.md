# jsk_docs

[![Build Status](https://travis-ci.org/jsk-ros-pkg/jsk_docs.svg?branch=master)](https://travis-ci.org/jsk-ros-pkg/jsk_docs)
[![Documentation Status](https://readthedocs.org/projects/jsk-docs/badge/?version=latest)](http://jsk-docs.readthedocs.org/en/latest/?badge=latest)

Document is available on [readthedocs.org](http://jsk-docs.readthedocs.org/en/latest/?badge=latest).


## How to add repository?

Add repository to the `doc/doc.rosinstall` file, the format follows [rosinstall format](http://docs.ros.org/independent/api/rosinstall/html/rosinstall_file_format.html)


## How to generate doc on local environment?

```bash
cd doc
source ./setup.sh
make html
make auto  # and go to http://127.0.0.1:8888
```

## How to trigger the build?

See https://readthedocs.org/dashboard/jsk-docs/integrations/9094/ to get the `TOKEN`.
It is added to the cron job at [Jenkins](http://jenkins.jsk.imi.i.u-tokyo.ac.jp) with root user.

```bash
curl -X POST -d "branches=master" -d "token=${TOKEN}" https://readthedocs.org/api/v2/webhook/jsk-docs/9094/
```
