#Zorba-CMD
Zorba-CMD is an interpreter that translates human language into shell commands

##History
The Zorba Project started in 2006, with a first version of zorba-cmd written in VisualBasic6 by Luca Tringali. Later in 2010 the interpreter has beeen translated in Python2, and in 2017 it has been adapted for Python3. Once published on TRingali's personal website, now it's hosted on GitHub.


##How does the dictionary work?
The dictionary is a *dict.csv* file in the folder *./lang/en-US/dict.csv*. Of course, you can create a dictionary for every language. It contains this kind of table:
```csv
ID;word;category;translation;couplewith;
1;install;verb;apt-get install $1;*;
2;(open(ed|s){0,1}|start|run);verb;$1 | dolphin $1 | gpio mode $1 out && gpio write $1 1 | dolphin $1;noun-program | noun-file | noun-GPIO-pin | *;
3;door;noun-GPIO-pin;18;open | close;
4;firefox;noun-program;/usr/bin/firefox;open;
5;(stop|close);verb;SET continuous FALSE | gpio mode $1 out && gpio write $1 0 | killall $1;noun-zorba | noun-GPIO-pin | *;
6;(zorba|you|computer);noun-zorba;zorba;*
7;temp;noun-file;/tmp/;open;
8;the;article;definitearticle;*;
9;a;article;indefinitearticle;*;
```
where:

- **ID** is a number that identifies a word. Now we don't really need it, but in the future we might want to use it for neural networks
- **word** is a regex that matches the word
- **category** is the kind of word: could be a verb, a article, or a noun. There are several kinds of nouns, in particular noun-zorba. noun-file, noun-program, and noun-GPIO-pin
- **translation** represents the possible translations: there could be more of them, because a word can have different meanings in different contexts. If this is a verb, the string *$1* will be replaced with a noun, which should act as a object of action (e.g.: in *apt-get install $1* it could be the name of a program to install)
- **couplewith** is the contexts where you can use this word: the order of the contexts must match the roder of the translations, and * means every context.


##Speech recognition

First of all, install sphinx using the bash script *./install-sphinx.sh*. If everything goes well, you can try the speech recognition program running:
```bash
chmod +x ./speechrecognition.py
./speechrecognition.py
```
It is possible to adapt the default language model to your voice using *-t* option ("t" means "training", even if this is not actually a full training but just an adaptation).