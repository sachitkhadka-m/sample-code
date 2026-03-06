echo "Fetching submodule data (Backend Main Team)"

cd module-main
git pull origin main

cd ..
git add module-main
git commit -m "submodule changes"
git push --recurse-submodules=check

echo 'Sucessfully fetched the data (Backend Main Team)'
