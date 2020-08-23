# WinAPIGraph

`WinAPIGraph` is a program based on neo4j, for the creation of software behavior graphs. `WinAPIGraph` uses the PyREBox sandbox to perform a dynamic analysis of the software and to obtain the trace of the API calls made by the software. 
The first thing to be done is to connect to the Neo4j database, once connected we proceed to read the log file provided by PyREBox.
Once the functions extracted from the analysis are read, they are processed by comparing them with the configuration files in the API_FILE directory. If they are found, this function and the arguments are compared with the Deviare2 database.
Deviare2_db is a widely used database containing the main APIs used by the programs. We will use this database to check that the DLLs, functions and arguments entered into the system are correct.
Once all the checks are done we can proceed to generate the network.
A bash script is also included for the automation of the whole system to which the malware to be analyzed must be introduced as well as the path to the compressed malware. Optionally, an address to which the obtained log will be written can be included and later `WinAPIGraph` will use it to generate the network.


# Install
	
`WinAPIGraph` uses py2neo to connect to the neo4j database, and Sqlite3 
for communication with the deviare2_db database.

```python
import py2neo
import Sqlite3
```

# Starting a Graph

`WinAPIGraph` starts a VM through PyREBox, once all the malware analysis is executed 
and the VM is closed the process of network creation will start, for this it is necessary 
to have the neo4j database active. The script can be started through ``start.sh``.

```
---------------------------------
Usage
---------------------------------

Options:
    -h, --help show brief help"
    -p, --path-malware=PATH  specify the path of the malware to be analyzed"
    -m, --malware=MALWARE specify a malware to analyze"
    -l, --path-logs=PATH  specify the path of the logs to generate a graph (DEFAULT:pyrebox/logs/function_calls.log)"

```


`WinAPIGraph` can also be run separately by simply entering the address where 
the log is located, from which we want to generate the network. ``python3 WinAPIGraph.py``.

```
---------------------------------
Usage
---------------------------------

Options:
    -h, --help show brief help"
    -f, --file=PATH  specify the path of the file of the logs

```
![alt text](git@github.com:f3rr4nx/WinAPIGraph.git/docs/media/WinAPI.png?style=centerme)


![alt text](git@github.com:f3rr4nx/WinAPIGraph.git/docs/media/graph.png?style=centerme)

./script.sh -p pyrebox/malware/ALINA_MOD.zip -m ALINA_MOD.exe -l pyrebox/logs/function_calls.log

./script.sh -p pyrebox/malware/ALINA_MOD.zip -m ALINA_MOD.exe
