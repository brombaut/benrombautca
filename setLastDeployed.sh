#!/usr/bin/env sh

rm "./src/footer/last-deployed.ts";
touch "./src/footer/last-deployed.ts";
currDate=$(date +'%d/%m/%Y');
echo "export default \"${currDate}\";" >> "./src/footer/last-deployed.ts";

git add ./src/footer/last-deployed.ts;