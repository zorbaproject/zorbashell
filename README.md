# ZorbaShell
ZorbaShell is an interpreter that translates human language into commands. It features an interactive shell for personal computers and a bot for Telegram

## History
The Zorba Project started in 2006, with a first version of zorba-cmd written in VisualBasic6 by Luca Tringali. Later in 2010 the interpreter has beeen translated in Python2, and in 2017 it has been adapted for Python3. Once published on Tringali's personal website, now it's hosted on GitHub.

## Installing and using Zorba
Please look at INSTALL.txt


## How does the dictionary work?
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


## Speech recognition
Speech recognition is based on Sphinx, you can adapt the vocal model to your voice using "-t" option.

## Watchme
There is a "watchme" folder in the source code of ZorbaShell. When a file is written (by any other program) in this folder, Zorba will notice it and read its contents to check for a message to send or a command to run. For example, you can set the command:
```bash
echo "Msg:It's time to wake up" > /root/zorbashell/watchme/wakeup.txt
```
to run every day at 8 o'clock with Cron, and you will get a message to wake from you night sleep. But you can also give a command, for example adding the line:
```bash
0 19 * * * root echo "CMD:open lights" > /root/zorbashell/watchme/lightson.txt
```
to /etc/crontab makes Zorba turn on the lights everyday at 19:00. Of course, the name you choose for a file to write in this folder is irrelevant.
You can also write your own script, for example to check every minute for new emails and send you a note when there are unread messages. Or an alert when a temperature sensor gives a value over 25°C.
