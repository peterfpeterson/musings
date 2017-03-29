#!/bin/sh
echo "looking for changes in $1/docs"
git diff --quiet $1/docs/AtlantaRagnar2017/plot.html
if [ $? ]; then
    echo atlanta data.json changed
    git commit $1/docs/AtlantaRagnar2017/* -m "Update from travis-ci"
    git push
fi
