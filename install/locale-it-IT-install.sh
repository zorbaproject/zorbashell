#!/bin/sh

#please run this with sudo
if [ "$(whoami)" == "root" ] ; then
    echo "You're root, good."
else
    echo "Please run this program with sudo."
    exit 1
fi


version="cmusphinx-it-5.2"
inst_dir="/usr/local/lib/python3.5/dist-packages/speech_recognition/pocketsphinx-data/it-IT"
acmodel_dir="voxforge_it_sphinx.cd_cont_2000"

#following instructions: https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst

wget https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Italian/$version.tar.gz/download
mv download $version.tar.gz

wget https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/Italian/it.tar.gz/download
mv download it.tar.gz

tar -xvf $version.tar.gz
tar -xvf it.tar.gz

cp ./$version/etc/voxforge_it_sphinx.lm ./italian.lm
sphinx_lm_convert -i ./italian.lm -o ./italian.lm.bin

mkdir $inst_dir
cp -r ./it $inst_dir/dictionary

cp ./italian.lm.bin $inst_dir/language-model.lm.bin

cp ./$version/etc/voxforge_it_sphinx.dic $inst_dir/pronounciation-dictionary.dict

mkdir $inst_dir/acoustic-model
cp -r ./$version/model_parameters/$acmodel_dir/* $inst_dir/acoustic-model/

#we may need to change "-cmn batch" in "-cmn current"
#sudo cp /usr/local/lib/python3.5/dist-packages/speech_recognition/pocketsphinx-data/it-IT/acoustic-model/feat.params /usr/local/lib/python3.5/dist-packages/speech_recognition/pocketsphinx-data/it-IT/acoustic-model/feat.paramsOLD

rm ./italian.lm.bin
rm ./italian.lm
rm $version.tar.gz
rm -r $version
rm -r ./it

apt-get install mbrola-it3 mbrola-it4

#wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/it3/it3-010304.zip
#wget http://www.tcts.fpms.ac.be/synthesis/mbrola/dba/it4/it4-010926.zip
