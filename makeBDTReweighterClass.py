import os
import sys
import zipfile
import shutil
import glob
import re

def main(pathToTreeLiteZip, outputClassName, multiplier, removeMissing, outputPath) :

    print "Getting", pathToTreeLiteZip
    zipf = zipfile.ZipFile(pathToTreeLiteZip, 'r')

    tempDir = outputPath+'/temp_'+outputClassName

    zipf.extractall(tempDir)
    zipf.close()

    print "Making", outputClassName, "with multiplier", multiplier
    
    if removeMissing :
        print "Removing checks for missing data."
    print "Writing to directory", outputPath

    outFileName = outputPath+'/'+outputClassName+'.h'
    
    originalFile = glob.glob(tempDir+'/*/main.c')[0]

    with open(outFileName,'w') as new_file:
        with open(originalFile) as old_file:
            for line in old_file:
                if '#include \"header.h\"' in line :
                    new_file.write('#include \"BDTReweighter.h\"\n')
                    new_file.write('class '+outputClassName+' : public BDTReweighter {\n')
                    new_file.write(' public :\n')
                    new_file.write(' '+outputClassName+'() : BDTReweighter('+multiplier+') {;}\n')
                    new_file.write('  ~'+outputClassName+'() {;}\n')
                elif 'float predict(union Entry* data, int pred_margin) {' in line :
                    new_file.write('   float predict(union BDTReweighter::BDTReweighterFeature* data, int pred_margin) {\n')
                elif removeMissing and '.missing' in line :
                    new_file.write(re.sub("\!\(data\[.*\].missing \!= -1\) \|\|", "", line) ) # There is a different "missing" statement that we need to take into account.
                else :
                    new_file.write(line)
            new_file.write('};\n')

    here  = os.path.dirname(os.path.realpath(__file__))

    try :
        shutil.copyfile(here+'/BDTReweighter.h', outputPath+'/BDTReweighter.h')
    except shutil.Error :
        print "Couldn't copy", here+'/BDTReweighter.h', 'to', outputPath+'/BDTReweighter.h'
        pass

    shutil.rmtree(tempDir)


if __name__ == "__main__" :


    if len(sys.argv) not in [4, 5, 6] :
        print "Usage:"
        print "makeBDTReweighterClass pathToTreeLiteZip outputClassName multiplier [remove missing] [outputPath]"
        exit(0)

    pathToTreeLiteZip = sys.argv[1]
    outputClassName = sys.argv[2]
    multiplier = sys.argv[3]

    if len(sys.argv) in [5,6] :
        removeMissing = bool(int(sys.argv[4]))
    else :
        removeMissing = False

    if len(sys.argv) == 6 :
        outputPath = sys.argv[5]
    else :
        outputPath = './'

    main(pathToTreeLiteZip = pathToTreeLiteZip, outputClassName = outputClassName, multiplier = multiplier, removeMissing = removeMissing, outputPath = outputPath)
