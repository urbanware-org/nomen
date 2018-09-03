#!/bin/bash

TESTDATA=/tmp/nomen_testdata_$$
TESTDIR=/tmp/nomen_testrun_$$

CFGLOWER=/tmp/nomen_lower_$$.cfg
CFGMIXED=/tmp/nomen_mixed_$$.cfg
CFGUPPER=/tmp/nomen_upper_$$.cfg

ls | grep "nomen-" &>/dev/null
if [ $? -ne 0 ]; then
    echo "Please run this script directly from the Nomen project directory."
    exit 1
else
    echo
    echo "This is a simple shell script to test the functionality of the different Nomen"
    echo "components. For details of each step see the script code."
    echo
    echo "Hit Return to proceed or Ctrl+C to cancel."
    read
fi

rm -fR $TESTDIR
rsync -a ./* ${TESTDIR}/

echo "lower"        >  $CFGLOWER
echo "mIxEd"        >  $CFGMIXED
echo "Upper"        >  $CFGUPPER

echo "\$(uLLiVaN)"  >> $CFGMIXED
echo "\$(GIL)"      >> $CFGLOWER
echo "\$('s )"      >> $CFGLOWER

echo
echo
echo
echo "=============================================================================="
figlet "Dir Spc Remover"
echo "Nomen Directory Space Remover"
echo "------------------------------------------------------------------------------"
EXCLUDE="doc"
BASEDIR="    Foo,Bar and Foobar feat.John Doe -Foo( Bar [  2000 ] )  "
SUBDIR="   Subdir  ,  Recursive   "
TEMP="${TESTDATA}/${BASEDIR}/${SUBDIR}"
rm -fR ${TESTDATA}/
mkdir -p "${TEMP}"
mkdir -p "${TESTDATA}/Stuff/no-spaces-around-dashes"
mkdir -p "${TESTDATA}/Stuff/no-spaces-yet-again"
find ${TESTDATA} | grep -v "^${TESTDATA}$" | sort
echo "------------------------------------------------------------------------------"
${TESTDIR}/nomen-dirspace.py -r -d ${TESTDATA} -s -l -t -b --hyphens -p --exclude "again;dash"
find ${TESTDATA} | grep -v "^${TESTDATA}$" | sort

echo
echo
echo
echo "=============================================================================="
figlet "File Name Mod"
echo "Nomen File Name Modifier"
echo "------------------------------------------------------------------------------"
rm -fR ${TESTDATA}/
mkdir -p ${TESTDATA}/Upper
touch ${TESTDATA}/test1.TXT
touch ${TESTDATA}/test2.Txt
touch ${TESTDATA}/test3.txt
touch ${TESTDATA}/test4.TXT
touch ${TESTDATA}/test4.Txt
touch ${TESTDATA}/test4.txt
touch ${TESTDATA}/test4.foobar.txt
touch ${TESTDATA}/test100.doc
touch ${TESTDATA}/Upper/test\ 1\ test.TXT
touch ${TESTDATA}/Upper/2\ test.Txt
touch ${TESTDATA}/Upper/test3test.txt
touch ${TESTDATA}/Upper/4test.TXT
touch ${TESTDATA}/Upper/test4.Txt
touch ${TESTDATA}/Upper/test4.txt
touch ${TESTDATA}/Upper/test200.doc
tree ${TESTDATA}
echo "------------------------------------------------------------------------------"
echo "Remove prefix 'test' and exclude file containing the string '${EXCLUDE}'"
echo
${TESTDIR}/nomen-filemod.py --confirm -r -d ${TESTDATA} -a remove -p any \
                            -s "test" --exclude "${EXCLUDE}" --strip " "
tree ${TESTDATA}

echo
echo
echo
echo "=============================================================================="
figlet "File Renamer"
echo "Nomen File Renamer"
echo "------------------------------------------------------------------------------"
RENAME_MODE="keep-order"
RENAME_STEP=2
EXCLUDE="doc"
rm -fR ${TESTDATA}/
mkdir -p ${TESTDATA}/Upper
touch ${TESTDATA}/test0
touch ${TESTDATA}/test1.TXT
touch ${TESTDATA}/test2.Txt
touch ${TESTDATA}/test3.txt
touch ${TESTDATA}/test4.TXT
touch ${TESTDATA}/test4.Txt
touch ${TESTDATA}/test4.txt
touch ${TESTDATA}/test4.foo.txt
touch ${TESTDATA}/johndoe.doc
touch ${TESTDATA}/Upper/test1.TXT
touch ${TESTDATA}/Upper/test2.Txt
touch ${TESTDATA}/Upper/test3.txt
touch ${TESTDATA}/Upper/test4.TXT
touch ${TESTDATA}/Upper/test4.Txt
touch ${TESTDATA}/Upper/test4.txt
touch ${TESTDATA}/Upper/johndoe.doc
tree ${TESTDATA}
echo "------------------------------------------------------------------------------"
echo "Use consecutive mode and exclude file containing the string '${EXCLUDE}'"
echo
touch ${TESTDATA}/test1.TXT
touch ${TESTDATA}/test2.Txt
touch ${TESTDATA}/test3.txt
touch ${TESTDATA}/test4.TXT
touch ${TESTDATA}/Upper/test1.TXT
touch ${TESTDATA}/Upper/test2.Txt
touch ${TESTDATA}/Upper/test3.txt
touch ${TESTDATA}/Upper/test4.TXT
${TESTDIR}/nomen-fileren.py --confirm -r -d ${TESTDATA} -m ${RENAME_MODE} --exclude "${EXCLUDE}" --step ${RENAME_STEP}
tree ${TESTDATA}

echo
echo
echo
echo "=============================================================================="
figlet "File Name Case"
echo "Nomen File Name Case Converter"
echo "------------------------------------------------------------------------------"
rm -fR ${TESTDATA}
mkdir -p ${TESTDATA}/sub
touch ${TESTDATA}/tEst1.TXT
touch ${TESTDATA}/tEst2.Txt
touch ${TESTDATA}/tEst3.txt
touch ${TESTDATA}/tEst4.TXT
touch ${TESTDATA}/tEst4.Txt
touch ${TESTDATA}/teSt4.txt
touch ${TESTDATA}/teST4.txt
touch ${TESTDATA}/test4.foo.txt
touch ${TESTDATA}/johndoe.doc
touch ${TESTDATA}/foobar
touch ${TESTDATA}/GILBERT\ O\'SULLIVAN\'S\ SONG.txt
touch ${TESTDATA}/LOWER\ MIXED\ TITLE\ UPPER.txt
touch ${TESTDATA}/sub/test1.TXT
touch ${TESTDATA}/sub/test2.Txt
touch ${TESTDATA}/sub/test3.txt
touch ${TESTDATA}/sub/test4.TXT
touch ${TESTDATA}/sub/test4.Txt
touch ${TESTDATA}/sub/test4.Txt
touch ${TESTDATA}/sub/johndoe.doc
touch ${TESTDATA}/sub/hansgruber.doc
touch ${TESTDATA}/sub/readme.doc
tree ${TESTDATA}
echo "------------------------------------------------------------------------------"
echo "Adjust file names to title case except for certain names (see case config) and"
echo "rename duplicates"
echo
${TESTDIR}/nomen-filecase.py --confirm -r -d ${TESTDATA} -m rename -c title \
                             --cfg-lower $CFGLOWER \
                             --cfg-mixed $CFGMIXED \
                             --cfg-upper $CFGUPPER
tree ${TESTDATA}

echo
echo
echo
echo "=============================================================================="
figlet "Ext Renamer"
echo "Nomen Extension Renamer"
echo "------------------------------------------------------------------------------"
rm -fR ${TESTDATA}
mkdir -p ${TESTDATA}/sub
touch ${TESTDATA}/test1.TXT
touch ${TESTDATA}/test2.Txt
touch ${TESTDATA}/test3.txt
touch ${TESTDATA}/test4.TXT
touch ${TESTDATA}/test4.Txt
touch ${TESTDATA}/test4.txt
touch ${TESTDATA}/test4.foo.txt
touch ${TESTDATA}/johndoe.doc
touch ${TESTDATA}/foobar
touch ${TESTDATA}/sub/test1.TXT
touch ${TESTDATA}/sub/test2.Txt
touch ${TESTDATA}/sub/test3.txt
touch ${TESTDATA}/sub/test4.TXT
touch ${TESTDATA}/sub/test4.Txt
touch ${TESTDATA}/sub/test4.txt
touch ${TESTDATA}/sub/johndoe.doc
tree ${TESTDATA}
echo "------------------------------------------------------------------------------"
echo "Adjust '*.txt' extensions (case-insensitive) to '*.renamed' and rename"
echo "duplicates"
echo
${TESTDIR}/nomen-extren.py --confirm -r -d ${TESTDATA} -m rename -e "TXT" -t "renamed"
tree ${TESTDATA}

echo
echo
echo
echo "=============================================================================="
figlet "Ext Case Conv"
echo "Nomen Extension Case Converter"
echo "------------------------------------------------------------------------------"
rm -fR ${TESTDATA}
mkdir -p ${TESTDATA}/sub
touch ${TESTDATA}/test1.TXT
touch ${TESTDATA}/test2.Txt
touch ${TESTDATA}/test3.txt
touch ${TESTDATA}/test4.TXT
touch ${TESTDATA}/test4.Txt
touch ${TESTDATA}/test4.txt
touch ${TESTDATA}/test4.foo.txt
touch ${TESTDATA}/johndoe.doc
touch ${TESTDATA}/foobar
touch ${TESTDATA}/sub/test1.TXT
touch ${TESTDATA}/sub/test2.Txt
touch ${TESTDATA}/sub/test3.txt
touch ${TESTDATA}/sub/test4.TXT
touch ${TESTDATA}/sub/test4.Txt
touch ${TESTDATA}/sub/test4.txt
touch ${TESTDATA}/sub/test4.TxT
touch ${TESTDATA}/sub/johndoe.doc
tree ${TESTDATA}
echo "------------------------------------------------------------------------------"
echo "Adjust extensions to lowercase and rename duplicates"
echo
${TESTDIR}/nomen-extcase.py --confirm -r -d ${TESTDATA} -m rename -c lower
tree ${TESTDATA}

echo
echo "=============================================================================="
echo

rm -fR $TESTDATA
rm -fR $TESTDIR
rm -f /tmp/nomen_*_$$.cfg

# EOF
