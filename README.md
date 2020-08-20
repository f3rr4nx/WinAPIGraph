# WinAPIGraph

`WinAPIGraph` is a program based on neo4j, for the creation of software behavior graphs. 
`WinAPIGraph` uses the PyREBox sandbox to perform a dynamic analysis of the software 
and to obtain the trace of the API calls made by the software.

Deviare2_db is a widely used database containing the main APIs used by the programs. 
`WinAPIGraph` will use this database to check that the DLLs, functions and arguments 
entered in the system are correct.

A bash script is also included for the automation of the whole system to which 
the malware to be analyzed must be introduced as well as the path to the compressed 
malware and optionally an address to which the log obtained will be written and which 
will later be used by `WinAPIGraph` to generate the network.


### Install
	
`WinAPIGraph` uses py2neo to connect to the neo4j database, and Sqlite3 
for communication with the deviare2_db database.

```python
import py2neo
import Sqlite3
```

### Starting a Graph

`WinAPIGraph` starts a VM through PyREBox, once all the malware analysis is executed 
and the VM is closed the process of network creation will start, for this it is necessary 
to have the neo4j database active. The script can be started through ``start.sh``.

`WinAPIGraph` can also be run separately by simply entering the address where 
the log is located, from which we want to generate the network. ``python3 WinAPIGraph.py``.




./script.sh -p pyrebox/malware/ALINA_MOD.zip -m ALINA_MOD.exe -l pyrebox/logs/function_calls.log

./script.sh -p pyrebox/malware/ALINA_MOD.zip -m ALINA_MOD.exe
