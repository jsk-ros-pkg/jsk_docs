jsk_docs [![Documentation Status](https://readthedocs.org/projects/jsk-docs/badge/?version=latest)](http://jsk-docs.readthedocs.org/en/latest/?badge=latest)
========

# how to add repository
```
cd doc
git submodule add http://github.com/jsk-ros-pkg/jsk_xxx jsk_xxx
```
and add that information to doc/index.rst

# how to update repository
```
cd doc
update_submodule.sh
git commit -m "update submodules for repository `LC_TIME=C date`" -a
```

# how to update doc directory
```
cd doc/jsk_xxx
../update_doc_link.sh
```
