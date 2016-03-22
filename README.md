jsk_docs [![Documentation Status](https://readthedocs.org/projects/jsk-docs/badge/?version=latest)](http://jsk-docs.readthedocs.org/en/latest/?badge=latest)
========
Document is available on [readthedocs.org](http://jsk-docs.readthedocs.org/en/latest/?badge=latest).


# how to add repository

add repository to the `doc/doc.rosinstall` file, the format follows [rosinstall format](http://docs.ros.org/independent/api/rosinstall/html/rosinstall_file_format.html)

# how to generate doc on local environment
```
cd doc
source ./setup.sh
make html
make auto  # and go to http://127.0.0.1:8888
```
