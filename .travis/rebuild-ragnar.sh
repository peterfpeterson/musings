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
else
    git checkout AtlantaRagnar2017/plot.html
fi

git diff --cached --quiet
if [ $? ]; then
    git commit -m "Update from travis-ci build $TRAVIS_BUILD_NUMBER"
    git remote add origin-master https://${GITHUB_TOKEN}@github.com/peterfpeterson/musings.git > /dev/null 2>&1
    git push --set-upstream origin-master master
fi

cd -
