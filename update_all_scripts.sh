cd ASE
for folder in Getting_Started Adsorption Transition_States
do
    cd $folder
    ./make_zips.sh
    cd ../
done
cd ../Scripts
./make_zips.sh
cd ../
git add *
git commit -m "udpated scripts"
git push
