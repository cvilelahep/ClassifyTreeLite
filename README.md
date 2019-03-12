## ClassifyTreeLite

This script takes the zipped output of treelite and produces a class that inherits from BDTReweighter.

# Usage
makeBDTReweighterClass pathToTreeLiteZip outputClassName multiplier [remove missing] [outputPath]

For example:
python makeBDTReweighterClass.py ~/DUNE/ValidateMCC11FakeData/ProtonEdepm20pc_trueKinBDT.zip ClassName 1. 1 ~/DUNE/ValidateMCC11FakeData/
The line above will take the zip in ~/DUNE/ValidateMCC11FakeData/ProtonEdepm20pc_trueKinBDT.zip and produces a class with ClassName, where the BDT output is multiplied by 1., and the checks for missing data entries are removed. The output class will be written in ~/DUNE/ValidateMCC11FakeData/.