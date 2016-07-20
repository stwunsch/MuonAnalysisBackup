# Check whether the file is executed in the same directory where it is placed

if [ ! -f cleanupSKIPs.sh ];
then
    echo "[ERROR] Please execute the script in the same folder where it is placed."
    exit 1
fi

# Delete all the generated SKIP files

read -p "[INFO] Are you sure that you want to remove all the generated SKIP files (type 'YES' to confirm)? " -r
if [[ $REPLY == YES ]]
then
    find . -name SKIP -delete
    echo "[INFO] All SKIP files are deleted."
else
    echo "[WARNING] Aborting skript."
fi
