#!/usr/bin/python

import sys, os, re

from optparse import OptionParser # Command line parsing
usage = "usage: %prog summary files"
version = "%prog."
parser = OptionParser(usage=usage,version=version)
parser.add_option("-p", "--printDataSets", action="store_true", dest="printDS", default=False, help="Print datasets without attempting to download.")
parser.add_option("-M", "--MC", action="store_true", dest="getMC", default=False, help="Get DQM files for MC campaign.")
parser.add_option("-D", "--DATA", action="store_true", dest="getDATA", default=False, help="Get DQM files for DATA campaign.")
(options, args) = parser.parse_args()

##Begin declaration of Functions

#getDataSets if used to discover and download the datasets. It is seperated as a function so that we can easily switch between
#MC and DATA datasets

def getDataSets( dsFlags = {'RelValMinBias_13TeV_pythia8__':'MinBias'},
                 curl = "/usr/bin/curl -O -L --capath %(CERT_DIR)s --key %(USER_PROXY)s --cert %(USER_PROXY)s https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelVal/%(relValDIR)s",
                 ofnBlank = "HcalRecHitValidationRelVal_%(sample)s_%(label)s_%(info)s.root",
                 label = "CMSSW_X_Y_Z",
                 slabel = "XYZ",
                 X509_CERT_DIR = os.getenv('X509_CERT_DIR', "/etc/grid-security/certificates"),
                 X509_USER_PROXY = os.getenv('X509_USER_PROXY'),
                 relValDIR = "CMSSW_?_?_x",
                 printDS = False,
                 camType = "MC"):
               
    print "Taking filenames from directory %s"%relValDIR

    # retrieve the list of datasets
    if not os.path.isfile(relValDIR):
        curlCommand = curl%{"CERT_DIR":X509_CERT_DIR, "USER_PROXY":X509_USER_PROXY, "relValDIR":relValDIR}
        print curlCommand
        os.system(curlCommand)

    # open raw input file 
    fin = open(relValDIR, "r")

    # loop over file and pull out lines of interest
    for line in fin:
        # limit to one entry per dataset
        if label in line:
            # select datasets of interest
            for str in dsFlags.keys():
                if str in line:
                    # extract dataset path
                    path = line.split('\'')[1].strip()
                    #print "Getting DQM output from dataset: %s"%path
                    print path
                    if printDS:
                        continue

                    # construct file name
                    fname = path.split("/")[-1]

                    # create file name for use with hcal scripts
                    info = fname.split("__")[2].replace(label, "").strip("-")

                    #The Data sample have an additional piece put in. We strip it out so that the MC and DATA code can be common

                    if camType == "DATA":
                        iparts = info.split("_")
			info = ""
			skip = False
			for fragment in iparts:
                            if skip:
                                info = info.strip("_")
                                skip = False
                                continue
                            if fragment == "RelVal":
                                skip = True
                                continue
                            info += fragment
                            info += "_"
                        info = info.strip("_")

                    ofn = ofnBlank%{"sample":dsFlags[str],"label":slabel,"info":info}
                
                    #Check if file exists already
                    if not os.path.isfile(ofn):
                        # copy file with curl
                        curlCommand = curl%{"CERT_DIR":X509_CERT_DIR,"USER_PROXY":X509_USER_PROXY, "relValDIR":relValDIR} + "/" + fname
                        print curlCommand
                        os.system(curlCommand)

                        # Rename file for use with HCAL scripts
                        mvCommand = "mv %(fn)s %(ofn)s"%{"fn":fname,"ofn":ofn}
                        print mvCommand
                        os.system(mvCommand)
                        print ""

    fin.close();
    rmCommand = "rm %(ofn)s"%{"ofn":relValDIR}
    print rmCommand
    os.system(rmCommand)

    if printDS:
        return

    # Copy the single pion scan part from Salavat's directory
    spFileName = "pi50scan%s_fullGeom_ECALHCAL_CaloTowers.root"%slabel
    cpCommand = "cp /afs/cern.ch/user/a/abdullin/public/pi50_scan/%s ."%spFileName
    if not os.path.isfile(spFileName):
        print cpCommand
        os.system(cpCommand)
        print ""

##End Functions



# This is a dictionary of flags to pull out the datasets of interest mapped to the desired name from the hcal script
dsMCFlags = {'RelValTTbar_13__':'TTbar', 'RelValQCD_Pt_80_120_13__':'QCD', 'RelValQCD_Pt_3000_3500_13__':'HighPtQCD', 'RelValMinBias_13TeV_pythia8__':'MinBias'}
#dsDATAFlags = {'191226__Jet__':'Jet', '149011__MinimumBias__':'MinBias'}
dsDATAFlags = {'191226__Jet__':'Jet', '208307__MinimumBias__':'MinBias'}
# filename prefix 
#fnPrefix = "DQM_V0001_R000000001"
#MinBiasPrefix = "DQM_V0001_R000149011"
#JetPrefix = "DQM_V0001_R000191226"

# blank curl command 
curlMC = "/usr/bin/curl -O -L --capath %(CERT_DIR)s --key %(USER_PROXY)s --cert %(USER_PROXY)s https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelVal/%(relValDIR)s"
curlDATA = "/usr/bin/curl -O -L --capath %(CERT_DIR)s --key %(USER_PROXY)s --cert %(USER_PROXY)s https://cmsweb.cern.ch/dqm/relval/data/browse/ROOT/RelValData/%(relValDIR)s"
# output file name blank
ofnBlank = "HcalRecHitValidationRelVal_%(sample)s_%(label)s_%(info)s.root"

# default release file for MC stub
#dfTextFile = "%s_%s.txt"
dfTextFile = "%s"

# ensure all required parameters are included
if len(args) < 1:
    print "Usage: ./RelValHarvest.py -M (or -D) fullReleaseName"
    print "fullReleaseName : CMSSW_7_4_0_pre8"
    exit(0)

#Make sure a Dataset is specified
if not options.getMC and not options.getDATA:
    print "You must specify a dataset:"
    print "    -M : Monte Carlo"
    print "    -D : Data"
    exit(0)

# gather input parameter
label     = args[0]

#Now we check if the release provided works
pattern = re.compile(r'CMSSW_\d{1,2}_\d{1,2}_\d{1,2}.*') #We are checking if the string begins with CMSSW_?_?_?, posibly with two digits in each position
match = pattern.match(label)
if match:
    slabel = match.group().replace('CMSSW','').replace("_","")
else:
    print label, " is an invalid CMMSW release name."
    print "Please provide a release name in the form: CMSSW_X_Y_Z"
    exit(0)

# gather necessary proxy info for curl
X509_CERT_DIR = os.getenv('X509_CERT_DIR', "/etc/grid-security/certificates")
X509_USER_PROXY = os.getenv('X509_USER_PROXY')

# modify label to shortened format (remove CMSSW and '_')
#slabel = label.replace('CMSSW','').replace("_","")

# get relval dir from label
clabel = label.split("_")
relValDIR = "%s_%s_%s_x"%(clabel[0], clabel[1], clabel[2])

if options.getMC:
    getDataSets( dsFlags = dsMCFlags,
                 curl = curlMC,
                 label = label,
                 slabel = slabel,
                 relValDIR = relValDIR,
                 printDS = options.printDS,
                 camType = "MC")

if options.getDATA:
    getDataSets( dsFlags = dsDATAFlags,
                 curl = curlDATA,
                 label = label,
                 slabel = slabel,
                 relValDIR = relValDIR,
                 printDS = options.printDS,
                 camType = "DATA")

