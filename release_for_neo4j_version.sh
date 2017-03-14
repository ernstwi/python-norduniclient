#! /bin/bash

set -e

TAG="neo4j-3.0"

git tag -d $TAG
git tag $TAG
git push -f origin $TAG

