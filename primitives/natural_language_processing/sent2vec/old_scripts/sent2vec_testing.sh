#!/bin/bash -e 

Datasets=('LL1_TXT_CLS_apple_products_sentiment' 'LL1_TXT_CLS_3746_newsgroup' 'LL1_TXT_CLS_airline_opinion')
mkdir test_pipeline
cd test_pipeline

# create text file to record scores and timing information
touch scores.txt
echo "DATASET, F1 SCORE, EXECUTION TIME" >> scores.txt

for i in "${Datasets[@]}"; do

  # generate and save pipeline + metafile
  python3 "../sent2vec_pipeline.py" $i

  # test and score pipeline
  start=`date +%s` 
  python3 -m d3m runtime -d /datasets/ -v / fit-score -m *.meta -p *.json -c scores.csv
  end=`date +%s`
  runtime=$((end-start))

  # copy pipeline if execution time is less than one hour
  if [ $runtime -lt 3600 ]; then
     echo "$i took less than 1 hour, copying pipeline"
     cp * ../
  fi

  # save information
  IFS=, read col1 score col3 col4 < <(tail -n1 scores.csv)
  echo "$i, $score, $runtime" >> scores.txt
  
  # cleanup temporary file
  rm *.meta
  rm *.json
  rm scores.csv
done