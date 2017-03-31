#!/bin/sh
direc=$(dirname $0)
cd $direc/../docs
direc=$(pwd)
echo looking for changes in $direc
git checkout master

if git diff --quiet -- $direc/AtlantaRagnar2017/data.json
then
    echo Atlanta2017/data.json changed
    git add $direc/AtlantaRagnar2017/
    CHANGED=true
fi

#if git commit -m "Update from travis-ci build $TRAVIS_BUILD_NUMBER"
#then
#    git remote add origin-master https://${GITHUB_TOKEN}@github.com/peterfpeterson/musings.git > /dev/null 2>&1
#    git push --set-upstream origin-master master
#fi

cd -
