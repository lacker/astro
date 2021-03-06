#! /bin/bash

# Initially copied from Lebofsky

basedir=/home/lacker/obs/target_logs
session=$1
fullpath=$basedir/$session
blocksize=134224384
secsperblock=0.17899
tmpfile=/tmp/parse_obs_log.$$

if [ ! -f $fullpath ]; then
  echo "no session: $fullpath"
  exit 0
fi

allnodes=`cut -c4-5 $fullpath | sort -n | uniq | awk '{printf("%s  ",$1)}'`

echo "#                                                        :  $allnodes"

firstscan=1
for timing in `awk -F/ '{print $NF}' $fullpath | cut -c1-17 | sort | uniq`; do
  if (( "$firstscan" == 1 )); then
    mjd=`echo $timing | awk -F_ '{print $2}'`
    mjdsecs=`echo $timing | awk -F_ '{print $3}'`
    firstscan=`echo $mjd $mjdsecs | awk '{printf("%d",(($1 - 40587.0) * 86400) + $2)}'`
  fi
  grep $timing $fullpath > $tmpfile
  target=`head -1 $tmpfile | awk '{print $3}'`
  scan=`head -1 $tmpfile | awk -F'.' '{print $1}' | awk -F_ '{print $NF}'`
  length=`head -1 $tmpfile | awk '{print $NF}' | awk -F'.' '{print $1}'`
  lengthinblocks=`echo $length $secsperblock | awk '{printf("%d",$1/$2)}'`

  nicedate=`date -d "@"$firstscan "+%D %T"`

  echo $firstscan $nicedate $target $length $lengthinblocks | awk '{printf("%s %s %s %14s %4d (%5d) :",$1,$2,$3,$4,$5,$6)}' # nicedate is two words
  
  targetnodes=""
  for node in $allnodes; do
      rawdata=`grep blc$node $tmpfile | awk '{print $4}' | awk -F_ '{print $NF}' | awk -F'.' '{print $2}'`
    if [ -z "$rawdata" ]; then
      targetnodes="$targetnodes ---"
    else
      leftoverbytes=`grep blc$node $tmpfile | awk '{print $6}'`
      leftoverblocks=`echo $leftoverbytes $blocksize | awk '{printf("%d",($1/$2))}'` 
      rawdatablocks=`echo $rawdata $leftoverblocks | awk '{print $1 * 128 + $2}'`
      percent=`echo $rawdatablocks $lengthinblocks | awk '{printf("%d",($1/$2)*100)}'`
      format=`echo $percent | awk '{printf("%3d",$1)}'`
      targetnodes="$targetnodes $format"
    fi
  done 
  rm $tmpfile
  echo "$targetnodes   $scan"
  firstscan=1
done
