#!/bin/sh
direc=$(dirname $0)
echo "looking for changes in $direc"
cd $direc/../docs
pwd
git diff --quiet AtlantaRagnar2017/data.json
if [ $? ]; then
    echo Atlanta2017/data.json changed
    git commit $1/docs/AtlantaRagnar2017/* -m "Update from travis-ci"
    git push
fi
cd -
