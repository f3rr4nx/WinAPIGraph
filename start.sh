#!/bin/bash
# -------------------------------------------------------------------------
#
#     Copyright (C) 2020  Fernando Heras Díez
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# -------------------------------------------------------------------------


BASEDIR=$(dirname "$0")
PYTHON_BIN=/usr/bin/python3
file=pyrebox/mw_monitor_run.json
path_wm='C:\\Users\\Fernando\\Desktop'


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
                *)
                        break
                        ;;
        esac
done

if [ -z "$logs" ]; then
   logs=pyrebox/logs/function_calls.log
fi


${PYTHON_BIN} -c "import sys, json; jsonFile = open('$file', 'r')
data = json.load(jsonFile)
jsonFile.close() # Close the JSON file

## Working with buffered content
path = {
        'files_path': '$path_wm',
        'main_executable': '$BASEDIR/$malware',
        'files_bundle': '$BASEDIR/$path_malware'
    }
tmp = data['general'] 
data['general'] = path

## Save our changes to JSON file
jsonFile = open('$file', 'w+')
jsonFile.write(json.dumps(data, indent=4))
jsonFile.close()
"
pushd \pyrebox 
source pyrebox_venv/bin/activate
./pyrebox-i386 -m 8192 -monitor stdio -usb -device usb-tablet -drive file=images/Win7/Win7x32.qcow2,index=0,media=disk,format=qcow2,cache=unsafe -netdev user,id=network0,smb=/samba/ -device rtl8139,netdev=network0 -loadvm alina

popd
pushd \WinAPIGraph 
${PYTHON_BIN} WinAPIGraph.py -f $BASEDIR./$logs
