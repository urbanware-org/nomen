#!/usr/bin/env bash

testdata=/tmp/nomen_testdata_$$
testdir=/tmp/nomen_testrun_$$

cfg_lower=/tmp/nomen_lower_$$.cfg
cfg_mixed=/tmp/nomen_mixed_$$.cfg
cfg_upper=/tmp/nomen_upper_$$.cfg

ls | grep "nomen-" &>/dev/null
if [ $? -ne 0 ]; then
    echo "Please run this script directly from the Nomen project directory."
    exit 1
else
    echo
    echo "This is a simple shell script to test the functionality of the different Nomen"
    echo "components. For details of each step see the script code."
    echo
    echo "Notice that it requires a case-sensitive filesystem (e.g. 'ext3') in order to"
    echo "work properly."
    echo
    echo "Hit Return to proceed or Ctrl+C to cancel."
    read
fi

rm -fR $testdir
rsync -a ./* $testdir/

echo "lower"        >  $cfg_lower
echo "mIxEd"        >  $cfg_mixed
echo "Upper"        >  $cfg_upper

echo "\$(uLLiVaN)"  >> $cfg_mixed
echo "\$(GIL)"      >> $cfg_lower
echo "\$('s )"      >> $cfg_lower

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mDir Spc Remover"
echo -e "Nomen Directory Space Remover\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
exclude="doc"
dir_base="    Foo,Bar and Foobar feat.John Doe -Foo( Bar [  2000 ] )  "
dir_sub="   Subdir  ,  Recursive   "
temp="$testdata/$dir_base/$dir_sub"
rm -fR $testdata
mkdir -p "$temp"
mkdir -p "$testdata/Stuff/no-spaces-around-hyphens"
mkdir -p "$testdata/Stuff/no-spaces-yet-again"
find $testdata | grep -v "^$testdata$" | sort
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
$testdir/nomen-dirspace.py -r -d $testdata -s -l -t -b --hyphens -p --exclude "again;hyphen"
find $testdata | grep -v "^$testdata$" | sort

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mFile Name Mod"
echo -e "Nomen File Name Modifier\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
rm -fR $testdata
mkdir -p $testdata/Upper
touch $testdata/test1.TXT
touch $testdata/test2.Txt
touch $testdata/test3.txt
touch $testdata/test4.TXT
touch $testdata/test4.Txt
touch $testdata/test4.txt
touch $testdata/test4.foobar.txt
touch $testdata/test100.doc
touch $testdata/Upper/test\ 1\ test.TXT
touch $testdata/Upper/2\ test.Txt
touch $testdata/Upper/test3test.txt
touch $testdata/Upper/4test.TXT
touch $testdata/Upper/test4.Txt
touch $testdata/Upper/test4.txt
touch $testdata/Upper/test200.doc
tree $testdata
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
echo "Remove prefix 'test' and exclude file containing the string '$exclude'"
echo
$testdir/nomen-filemod.py --confirm -r -d $testdata -a remove -p any \
                            -s "test" --exclude "$exclude" --strip " "
tree $testdata

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mFile Renamer"
echo -e "Nomen File Renamer\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
rename_mode="keep-order"
rename_step=2
exclude="doc"
rm -fR $testdata
mkdir -p $testdata/Upper
touch $testdata/test0
touch $testdata/test1.TXT
touch $testdata/test2.Txt
touch $testdata/test3.txt
touch $testdata/test4.TXT
touch $testdata/test4.Txt
touch $testdata/test4.txt
touch $testdata/test4.foo.txt
touch $testdata/johndoe.doc
touch $testdata/Upper/test1.TXT
touch $testdata/Upper/test2.Txt
touch $testdata/Upper/test3.txt
touch $testdata/Upper/test4.TXT
touch $testdata/Upper/test4.Txt
touch $testdata/Upper/test4.txt
touch $testdata/Upper/johndoe.doc
tree $testdata
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
echo "Use consecutive mode and exclude file containing the string '$exclude'"
echo
touch $testdata/test1.TXT
touch $testdata/test2.Txt
touch $testdata/test3.txt
touch $testdata/test4.TXT
touch $testdata/Upper/test1.TXT
touch $testdata/Upper/test2.Txt
touch $testdata/Upper/test3.txt
touch $testdata/Upper/test4.TXT
$testdir/nomen-fileren.py --confirm -r -d $testdata -m $rename_mode --exclude "$exclude" --step $rename_step
tree $testdata

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mFile Name Case"
echo -e "Nomen File Name Case Converter\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
rm -fR $testdata
mkdir -p $testdata/sub
touch $testdata/tEst1.TXT
touch $testdata/tEst2.Txt
touch $testdata/tEst3.txt
touch $testdata/tEst4.TXT
touch $testdata/tEst4.Txt
touch $testdata/teSt4.txt
touch $testdata/teST4.txt
touch $testdata/test4.foo.txt
touch $testdata/johndoe.doc
touch $testdata/foobar
touch $testdata/GILBERT\ O\'SULLIVAN\'S\ SONG.txt
touch $testdata/LOWER\ MIXED\ TITLE\ UPPER.txt
touch $testdata/sub/test1.TXT
touch $testdata/sub/test2.Txt
touch $testdata/sub/test3.txt
touch $testdata/sub/test4.TXT
touch $testdata/sub/test4.Txt
touch $testdata/sub/test4.Txt
touch $testdata/sub/johndoe.doc
touch $testdata/sub/hansgruber.doc
touch $testdata/sub/readme.doc
tree $testdata
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
echo "Adjust file names to title case except for certain names (see case config) and"
echo "rename duplicates"
echo
$testdir/nomen-filecase.py --confirm -r -d $testdata -m rename -c title \
                             --cfg-lower $cfg_lower \
                             --cfg-mixed $cfg_mixed \
                             --cfg-upper $cfg_upper
tree $testdata

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mExt Renamer"
echo -e "Nomen Extension Renamer\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
rm -fR $testdata
mkdir -p $testdata/sub
touch $testdata/test1.TXT
touch $testdata/test2.Txt
touch $testdata/test3.txt
touch $testdata/test4.TXT
touch $testdata/test4.Txt
touch $testdata/test4.txt
touch $testdata/test4.foo.txt
touch $testdata/johndoe.doc
touch $testdata/foobar
touch $testdata/sub/test1.TXT
touch $testdata/sub/test2.Txt
touch $testdata/sub/test3.txt
touch $testdata/sub/test4.TXT
touch $testdata/sub/test4.Txt
touch $testdata/sub/test4.txt
touch $testdata/sub/johndoe.doc
tree $testdata
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
echo "Adjust '*.txt' extensions (case-insensitive) to '*.renamed' and rename"
echo "duplicates"
echo
$testdir/nomen-extren.py --confirm -r -d $testdata -m rename -e "TXT" -t "renamed"
tree $testdata

echo
echo
echo
echo -e "\e[93m==============================================================================\e[0m"
echo -e "\e[92mExt Case Conv"
echo -e "Nomen Extension Case Converter\e[0m"
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
rm -fR $testdata
mkdir -p $testdata/sub
touch $testdata/test1.TXT
touch $testdata/test2.Txt
touch $testdata/test3.txt
touch $testdata/test4.TXT
touch $testdata/test4.Txt
touch $testdata/test4.txt
touch $testdata/test4.foo.txt
touch $testdata/johndoe.doc
touch $testdata/foobar
touch $testdata/sub/test1.TXT
touch $testdata/sub/test2.Txt
touch $testdata/sub/test3.txt
touch $testdata/sub/test4.TXT
touch $testdata/sub/test4.Txt
touch $testdata/sub/test4.txt
touch $testdata/sub/test4.TxT
touch $testdata/sub/johndoe.doc
tree $testdata
echo -e "\e[90m------------------------------------------------------------------------------\e[0m"
echo "Adjust extensions to lowercase and rename duplicates"
echo
$testdir/nomen-extcase.py --confirm -r -d $testdata -m rename -c lower
tree $testdata

echo
echo -e "\e[93m==============================================================================\e[0m"
echo

rm -fR $testdata
rm -fR $testdir
rm -f /tmp/nomen_*_$$.cfg
