#!/bin/sh
direc=$(dirname $0)
echo looking for changes in $direc

# check for changes in files
if output=$(git status --porcelain docs/AtlantaRagnar2017/data.json) && [ -z "$output" ]; then
    echo Atlanta2017/data.json did not change
else
    echo Atlanta2017/data.json changed
    git add docs/AtlantaRagnar2017/
    CHANGED=true
    echo "something interesting changed"
fi

# if things have been staged then commit and push them
if git commit -m "Update from travis-ci build $TRAVIS_BUILD_NUMBER"
then
    git checkout master
    git remote add origin-master https://${GITHUB_TOKEN}@github.com/peterfpeterson/musings.git > /dev/null 2>&1
    git push --set-upstream origin-master master
fi
