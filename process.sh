#!/bin/bash

# Create log file
time=$(date +%Y%m%d_%H%M)
scpt_hm=$(cd $(dirname $0); pwd)
LOG_PATH="${scpt_hm}/logs"

ls -ld ${LOG_PATH}
if [ $? -ne 0 ]; then
    echo "${LOG_PATH} does not exist.. creating the same"
    mkdir -p ${LOG_PATH}
    if [ $? -eq 0 ]; then
        chmod 775 ${LOG_PATH}
        echo "${LOG_PATH} creation successful"
    else
        echo "${LOG_PATH} creation failed"
    fi
fi

LOG_FILE=${LOG_PATH}/${SCRIPT_NAME}_${time}.log
touch ${LOG_FILE}
chmod -R 775 ${LOG_FILE}
if [ $? -ne 0 ]; then
    echo "${LOG_FILE} creation failed"
fi

echo $'\n'"Start time: $(date +%Y%m%d_%H%M)" | tee -a ${LOG_FILE}
echo $'\n'"Running ${SCRIPT_NAME}.sh..." | tee -a ${LOG_FILE}
echo $'\n###################################################' | tee -a ${LOG_FILE}

# # run the reddit script
echo $'\n'"Running reddit_extractor.py..." | tee -a ${LOG_FILE}
python Reddit/reddit_extractor.py Reddit/subreddits.txt ./config.ini
exit_status=$?

if [ $exit_status -eq 0 ]; then
    echo "Script ran successfully" | tee -a ${LOG_FILE}
else
    echo "Script failed with exit code ${exit_status}" | tee -a ${LOG_FILE}
fi

# run the twitter script
echo $'\n'"Running twitter_extractor.py..." | tee -a ${LOG_FILE}
python Twitter/twitter_extractor.py Twitter/twitter_search.txt ./config.ini
exit_status=$?

if [ $exit_status -eq 0 ]; then
    echo "Script ran successfully" | tee -a ${LOG_FILE}
else
    echo "Script failed with exit code ${exit_status}" | tee -a ${LOG_FILE}
fi

echo $'\n###################################################' | tee -a ${LOG_FILE}

echo $'\n'"End time: $(date +%Y%m%d_%H%M)" | tee -a ${LOG_FILE}

echo $'\n'"Script ended successfully." | tee -a ${LOG_FILE}