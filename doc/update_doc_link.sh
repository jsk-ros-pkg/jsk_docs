#!/bin/bash

#set -x
set -e

[ -e doc ] || (echo "doc does not exists"; exit)

for readme in `find -name README.md -prune -print`; do
    if [ ! -e doc/$readme ]; then
        echo $readme
        #echo "doc/$readme does not exist, so creating doc/`dirname $readme` ..."
        dirname=`dirname $readme`
        filename=`basename $readme`
        mkdir -p doc/$dirname
        # echo "org: $readme"
        # echo "dir: $dirname"
        # echo "pat: `echo $dirname/ | sed 's@[^/]*/@../@g'`"
        # echo "   : `echo $readme | sed 's@^./@@'`"
        # echo "     ln -sf `echo $dirname/ | sed 's@[^/]*/@../@g'`$readme doc/`echo $readme | sed 's@^./@@'`"
        readme=`echo $readme | sed 's@^./@@'`
        ln -sf `echo $dirname/ | sed 's@[^/]*/@../@g'`$readme doc/$readme
        #ls -al doc/$readme
        #git add doc/$readme
    fi
done

reponame=$(basename `git rev-parse --show-toplevel`)

cat <<EOF > doc/index.rst
========
${reponame}
========

${reponame} is a stack for the packages which are used in JSK lab.

The code is open source, and \`available on github\`_.

.. _available on github: http://github.com/jsk-ros-pkg/${reponame}

This repository contains following ros packages:


.. toctree::
   :glob:
   :maxdepth: 2

EOF

for readme in `find doc -name README.md -prune -print | sort -r`; do
    echo $readme | sed "s@doc/@   @" >> doc/index.rst
done

cat doc/index.rst


