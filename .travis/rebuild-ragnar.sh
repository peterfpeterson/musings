#!/bin/bash
direc=$(dirname $0)
git checkout master
echo looking for changes in $direc

# check for changes in files
function add_if_changed
{
    if output=$(git status --porcelain "docs/races/${1}/data.json") && [ -z "$output" ]; then
        echo "${1}/data.json did not change"
    else
        echo "${1}/data.json changed"
        git add "docs/races/${1}/"
    fi
}

add_if_changed "2017/AtlantaRagnar"

# if things have been staged then commit and push them
if git commit -m "Update from travis-ci build $TRAVIS_BUILD_NUMBER"
then
    git remote add origin-master https://${GITHUB_TOKEN}@github.com/peterfpeterson/musings.git > /dev/null 2>&1
    git push --set-upstream origin-master master
fi
