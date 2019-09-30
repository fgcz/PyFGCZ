rem fcc converter script for generating mzXML using msconvert
rem Christian Panse <cp@fgcz.ethz.ch> 2019-09-27

"C:\Program Files (x86)\ProteoWizard\ProteoWizard 3.0.10200\msconvert" %1 --mzXML -o %~dp1\msconvert_mzXML

rem see also https://stackoverflow.com/questions/659647/how-to-get-folder-path-from-file-path-with-cmd/659672
