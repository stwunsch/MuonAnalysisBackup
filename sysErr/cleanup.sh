# Check whether the file is executed in the same directory where it is placed

if [ ! -f cleanup.sh ];
then
    echo "[ERROR] Please execute the script in the same folder where it is placed."
    exit 1
fi

# Delete all the generated files

read -p "Are you sure that you want to remove all the generated files (type 'YES' to confirm)? " -r
if [[ $REPLY == YES ]]
then
    find . -name *.root -delete
    rm -f nVtx.png
    find . -name SKIP -delete
fi
