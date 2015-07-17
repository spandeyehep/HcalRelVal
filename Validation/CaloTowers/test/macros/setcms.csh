############################################################################
#
# source this file to setup cms runtime environment (e.g. to access root) 
# File  : setcms.csh
# Author: Hans wenzel
# wenzel@fnal.gov
#
############################################################################
unsetenv CMS_PATH

if (!(${?CMS_PATH})) then 
setenv PATH ${PATH}:/cvmfs/cms.cern.ch/common
setenv CMS_PATH /cvmfs/cms.cern.ch
# source /uscmst1/prod/sw/cms/cshrc uaf
# source /uscmst1/prod/sw/cms/cshrc prod
source $CMS_PATH/cmsset_default.csh     
endif

#setenv  SCRATCH "/uscms_data/d1/$USER"
#setenv  SCRATCH3DAY "/uscmst1b_scratch/lpc1/3DayLifetime/$USER"
#cmscvsroot CMSSW
#echo "--> CVSROOT      "$CVSROOT

#source /uscmst1/prod/grid/CRAB_2_2_0/crab.csh
#source /uscmst1/prod/grid/CRAB_2_6_4/crab.csh
#source /uscmst1/prod/grid/CRAB_2_6_6/crab.csh
#source /uscmst1/prod/grid/CRAB_2_8_6/crab.csh
#source /uscmst1/prod/grid/CRAB_2_10_4_patch4/crab.csh 
#source /uscmst1/prod/grid/CRAB/crab.csh
#echo "--> CRABDIR      "$CRABDIR

#source $CMS_PATH/crab3/crab.csh    

#project CMSSW

#source /uscmst1/prod/grid/gLite_SL5.csh 

