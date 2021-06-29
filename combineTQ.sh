#! /bin/sh
 
#--------------- Setup inputs ---------------------
mass=${1:-"26"}
outdir1="TQ-rootfiles/"
outdir2="TQ-jsons/"
if [ ! -d "$outdir1" ]; then
  mkdir $outdir1
fi
if [ ! -d "$outdir2" ]; then
  mkdir $outdir2
fi

#---------------- Run combine ----------------------

for m in 26
do
  card="datacard_m${m}_2mu2e_2018.txt"
  combine -M AsymptoticLimits -m ${m} -d ${card}  -n .limit 
done

mv higgsCombine.limit.AsymptoticLimits.mH*.root ${outdir1} 

#---------------- Make jsons -------------------------
for m in 26
do
  name="${outdir2}datacard_m${m}_2mu2e_2018.json"
  combineTool.py -M CollectLimits ${outdir1}higgsCombine.limit.AsymptoticLimits.mH${m}.root  -o "${name}"
  echo Made json: ${name} 
done
