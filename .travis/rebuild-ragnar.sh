#!/bin/sh
direc=$(dirname $0)
cd $direc/../docs
pwd
echo "looking for changes in $direc"
git diff --quiet AtlantaRagnar2017/data.json
if [ $? ]; then
    echo Atlanta2017/data.json changed
    git commit $1/docs/AtlantaRagnar2017/* -m "Update from travis-ci"
    git push
fi
cd -
