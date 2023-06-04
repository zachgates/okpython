#!/bin/zsh
CELLAR=$(brew --cellar)
for PACKAGE in $(find $CELLAR -maxdepth 1 -type d -name "python@3.*"); do
    KEG=$(echo $PACKAGE/*)
    FRAMEWORK=$(echo $KEG/Frameworks/Python.framework)
    HEADERS=$(echo $FRAMEWORK/Versions/Current/Headers)
    INCLUDE=$(dirname $HEADERS)/$(stat -f "%Y" $HEADERS)
    {
    echo "---"
    echo "formula : !!str $(basename $PACKAGE)"
    echo "keg     : !!str $(basename `echo $PACKAGE/*`)"
    echo "headers : !!map"
    for HEADER in $(find $INCLUDE -name "*.h"); do
        SYMBOLS=$(grep -oe 'PyAPI_DATA(PyTypeObject) [^;]*' $HEADER)
        if [[ $SYMBOLS ]]; then
            echo
            echo "    ? !!str \"${HEADER:${#INCLUDE}+1}\""
            echo "    : !!seq ["
            for SYMBOL in $(echo $SYMBOLS | xargs -n2 zsh -c 'echo $1'); do
            echo "        $SYMBOL,"
            done
            echo "    ]"
        fi
    done
    } | tee "$1/$(basename $PACKAGE).yaml"
done
