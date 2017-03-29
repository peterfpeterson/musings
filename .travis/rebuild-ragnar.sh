#!/bin/sh
eval "$(ssh-agent -s)" #start the ssh agent
chmod 600 .travis/deploy_key.pem # this key should have push access
ssh-add .travis/deploy_key.pem

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
