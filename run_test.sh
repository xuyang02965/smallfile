#!/bin/bash   

TEST_INTERVAL=10
WORK_DIR=$1
OUTPUT_DIR="$2/"${WORK_DIR//\//_}
echo "Working dir is $WORK_DIR"
[ -e ${WORK_DIR} ] || mkdir -p ${WORK_DIR}
echo "Output dir is $OUTPUT_DIR"
[ -e ${OUTPUT_DIR} ] || mkdir -p ${OUTPUT_DIR}

FILESZ=1024
FILENUM=100
OPTYPES=("create" "append" "read" "delete")
#OPTYPES=("create" "delete")
#BLKSZ=(4 8 16 64 128)
BLKSZ=(4 8 16)
#BLKSZ=(4)
USER_NUM=(4 8 16)
#USER_NUM=(16)

for usrnum in ${USER_NUM[*]};
do
    for blksz in ${BLKSZ[*]};
    do
        for optype in ${OPTYPES[*]};
        do
           #echo $optype $blksz $usrnum 
	   python smallfile_cli.py --operation ${optype} --threads ${usrnum} --file-size ${FILESZ} --files ${FILENUM} --top ${WORK_DIR} --output-json ${OUTPUT_DIR}/${optype}_${usrnum}_${blksz}_${FILESZ}_${FILENUM}_output.json --response-times Y
        done
    done
done

