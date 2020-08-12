#!/bin/bash

while test $# -gt 0; do
        case "$1" in
                -h|--help)
                        echo "$package - attempt to capture frames"
                        echo " "
                        echo "$package [options] application [arguments]"
                        echo " "
                        echo "options:"
                        echo "-h, --help                show brief help"
                        echo "-p, --path-malware=PATH   specify the path of the malware to be analyzed"
                        echo "-m, --malware=MALWARE     specify a malware to analyze"
                        echo "-l, --path-logs=PATH      specify the path of the logs to generate a graph (DEFAULT:pyrebox/logs/function_calls.log)"
                        exit 0
                        ;;
                -p)
                        shift
                        if test $# -gt 0; then
                                path_malware=$1
                        else
                                echo "no path malware specified"
                                exit 1
                        fi
                        shift
                        ;;
                --path-malware*)
                        path_malware=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                -m)
                        shift
                        if test $# -gt 0; then
                                malware=$1
                        else
                                echo "no malware specified"
                                exit 1
                        fi
                        shift
                        ;;
                --malware*)
                        malware=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                -l)
                        shift
                        if test $# -gt 0; then
                                logs=$1
                        else
                                echo "no output dir specified"
                                exit 1
                        fi
                        shift
                        ;;
                --path-logs*)
                        logs=`echo $1 | sed -e 's/^[^=]*=//g'`
                        shift
                        ;;
                -i)
                        shift
                        if test $# -gt 0; then
                                image=$1
                                snapshot=$2
                        else
                                echo "no output dir specified"
                                exit 1
                        fi
                        shift
                        ;;
                --image*)
                        image=`echo $1 | sed -e 's/^[^=]*=//g'`
                        snapshot=$2
                        shift
                        ;;
                *)
                        break
                        ;;
        esac
done

if [ -z "$logs" ]; then
   logs=pyrebox/logs/function_calls.log
fi

BASEDIR=$(dirname "$0")
file=pyrebox/mw_monitor_run.json
path_wm='C:\\Users\\Fernando\\Desktop'


python3 -c "import sys, json; jsonFile = open('$file', 'r')
data = json.load(jsonFile)
jsonFile.close() # Close the JSON file

## Working with buffered content
path = {
        'files_path': '$path_wm',
        'main_executable': '$malware',
        'files_bundle': '$BASEDIR$path_malware'
    }
tmp = data['general'] 
data['general'] = path

## Save our changes to JSON file
jsonFile = open('$file', 'w+')
jsonFile.write(json.dumps(data, indent=4))
jsonFile.close()
"
cd pyrebox
$BASEDIR/pyrebox-i386 -monitor stdio -net none -m 256 -usb -device usb-tablet -drive file=$image,index=0,media=disk,format=qcow2,cache=unsafe -vnc 127.0.0.1:0 -loadvm $snapshot

cd ..
cd py2Graph
 python3 py2graph.py -f $BASEDIR./$logs
