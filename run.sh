#!/usr/bin/env bash
if [[ $1 == "" ]]; then
    echo "arg1 - full path to the test file (eg. tmp.csv)"
    exit
fi

currentDir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

inputProj=$currentDir"/projects"
result="$currentDir/Output.csv"

while read line
do
    slug=$(echo $line | cut -d, -f1)
    sha=$(echo $line | cut -d, -f2)
    module=$(echo $line | cut -d, -f3)
    test_name=$(echo $line | cut -d, -f4)
    crit_point=$(echo $line | cut -d, -f5 | cut -d'~' -f1)
    barrier_point=$(echo $line | cut -d, -f6)
    threshold=$(echo $line | cut -d, -f7)
    git clone "https://github.com/$slug" $inputProj/$slug 
	cd $inputProj/$slug 
	git checkout $sha 
    echo "$(echo $line | cut -d',' -f1-4)" >> $result
	cut_class=$(echo $crit_point | rev | cut -d'#' -f2 |  cut -d'$' -f2 | cut -d'/' -f1 | rev)
	cut_line_number=$(echo $crit_point | rev | cut -d'#' -f1 | rev)
	test_class=$(echo $barrier_point | rev | cut -d'#' -f2 |  cut -d'$' -f2 | cut -d'.' -f1 | rev)
	test_line_number=$(echo $barrier_point | rev | cut -d'#' -f1 | rev)
    echo $test_class
    input_file_cut=$(find -name "${cut_class}.java")
    input_file_test=$(find -name "${test_class}.java")
   	python3 "$currentDir/find_method.py" "$input_file_cut" "$cut_line_number"
   	python3 "$currentDir/find_method.py" "$input_file_test" "$test_line_number"

    #Modified CUT
   	python3 "$currentDir/find_method.py" "$input_file_cut" "$cut_line_number" $threshold "cut"

    #Modified TestCode
   	python3 "$currentDir/find_method.py" "$input_file_test" "$test_line_number" $threshold "test_code"
    echo "" >> $result
done < $1 #Fix-Result.csv
