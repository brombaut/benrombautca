#!/usr/bin/env sh

rm "./src/footer/last-deployed.ts"
touch "./src/footer/last-deployed.ts"
currDate=$(date +'%d/%m/%Y')
echo "export default \"${currDate}\";" >> "./src/data/last-deployed.ts"

git add -A
git commit -m "Updating last deployed"
git push

# abort on errors
set -e

# build
npm run build

cd dist

git init
git add -A
git commit -m 'deploy'

# if you are deploying to https://<USERNAME>.github.io/<REPO>
git push -f git@github.com:brombaut/benrombautca.git master:gh-pages

cd -