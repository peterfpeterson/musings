#!/bin/sh
direc=$(dirname $0)
echo "looking for changes in $direc"
cd $direc/../docs
pwd
git checkout master

git diff --quiet AtlantaRagnar2017/data.json
if [ $? ]; then
    echo Atlanta2017/data.json changed
    git add AtlantaRagnar2017/*
fi

git diff --cached --quiet
if [ $? ]; then
    git commit -m "Update from travis-ci build $TRAVIS_BUILD_NUMBER"
    git remote add origin https://${GH_TOKEN}@github.com/peterfpeterson/musings.git > /dev/null 2>&1
    git push
fi

cd -
