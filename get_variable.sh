for i in $(seq 2019 2021);
do wget --no-check-certificate https://pscfiles.apl.washington.edu/zhang/PIOMAS/data/v2.1/heff/heff.H$i.gz;
wget --no-check-certificate https://pscfiles.apl.washington.edu/zhang/PIOMAS/data/v2.1/gice/gice.H$i.gz
#do wget https://pscfiles.apl.washington.edu/zhang/PIOMAS/data/v2.1/heff/heff.H$i.gz
done
