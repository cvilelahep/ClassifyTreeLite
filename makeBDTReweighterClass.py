import os
import sys
import zipfile
import shutil
import glob
import re

def main(pathToTreeLiteZip, outputClassName, multiplier, removeMissing, outputPath, n_trees) :

    # Regular expression to search for top-level if blocks:
    topif_pattern = re.compile(r'\s*?if.*?}\s*?(?:(?=if)|(?=sum))', re.DOTALL | re.MULTILINE)

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
            
            # First read the entire file in and remove last (ALL-N) top-level if blocks
            old_file_text = old_file.read()

            if (n_trees) :
                print "Keeping only first", n_trees, "trees."

                top_ifs = topif_pattern.findall(old_file_text)
                all_trees = len(top_ifs)
                
                print "Total number of trees:", all_trees
                
                for i in range(n_trees, all_trees) :
                    print "Removing tree", i
                    print top_ifs[i], '\n\n'
                    old_file_text = re.sub(re.escape(top_ifs[i]), '', old_file_text)

            for line in old_file_text.splitlines():
                if '#include \"header.h\"' in line :
                    new_file.write('#include \"BDTReweighter.h\"\n')
                    new_file.write('class '+outputClassName+' : public BDTReweighter {\n')
                    new_file.write(' public :\n')
                    new_file.write(' '+outputClassName+'() : BDTReweighter('+multiplier+') {;}\n')
                    new_file.write('  ~'+outputClassName+'() {;}\n')
                elif 'float predict(union Entry* data, int pred_margin) {' in line :
                    new_file.write('   float predict(union BDTReweighter::BDTReweighterFeature* data, int pred_margin) {\n')
                elif removeMissing and ('.missing' in line) and ('||' in line) :
                    new_file.write(re.sub("\!\(data\[.*\].missing \!= -1\) \|\|", "", line) )
                elif removeMissing and ('.missing' in line) and ('&&' in line) :
                    new_file.write(re.sub("\\(data\[.*\].missing \!= -1\) \&\&", "", line) )
                else :
                    new_file.write(line)
                new_file.write('\n')
            new_file.write('};\n')

    here  = os.path.dirname(os.path.realpath(__file__))

    try :
        shutil.copyfile(here+'/BDTReweighter.h', outputPath+'/BDTReweighter.h')
    except shutil.Error :
        print "Couldn't copy", here+'/BDTReweighter.h', 'to', outputPath+'/BDTReweighter.h'
        pass

    shutil.rmtree(tempDir)


if __name__ == "__main__" :


    if len(sys.argv) not in [4, 5, 6, 7] :
        print "Usage:"
        print "makeBDTReweighterClass pathToTreeLiteZip outputClassName multiplier [remove missing] [outputPath] [N trees]"
        exit(0)

    pathToTreeLiteZip = sys.argv[1]
    outputClassName = sys.argv[2]
    multiplier = sys.argv[3]

    if len(sys.argv) in [5,6,7] :
        removeMissing = bool(int(sys.argv[4]))
    else :
        removeMissing = False

    if len(sys.argv) in [6,7] :
        outputPath = sys.argv[5]
    else :
        outputPath = './'

    if len(sys.argv) == 7 :
        n_trees = int(sys.argv[6])
    else :
        n_trees = 0

    main(pathToTreeLiteZip = pathToTreeLiteZip, outputClassName = outputClassName, multiplier = multiplier, removeMissing = removeMissing, outputPath = outputPath, n_trees = n_trees)
