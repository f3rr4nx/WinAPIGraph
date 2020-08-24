# WinAPIGraph

`WinAPIGraph` is a program based on neo4j for the generation of software behaviour graphs. `WinAPIGraph` uses the [PyREBox sandbox](https://github.com/Cisco-Talos/pyrebox.git) to perform a dynamic analysis of the software and to obtain the trace of the API calls made by the software. 

The first thing to do is to connect to the Neo4j database. Once connected we proceed to read the log file provided by PyREBox.
Once the functions extracted from the analysis are read, they are processed by comparing them with the configuration files in the [API_FILE](/WinAPIGraph/API_Files/) directory. If they are found, this function and the arguments are compared with the [Deviare2 database](https://github.com/nektra/Deviare2.git).
Deviare2_db is a widely used database that contains the main APIs used by the programs. We will use this database to check that the DLLs, the functions and the arguments entered into the system are correct.

Once all the checks are done we can proceed to generate the network.
A bash script is also included for the automation of the whole system to which the malware to be analyzed must be introduced as well as the path to the compressed malware. Optionally, an address to which the obtained log will be written can be included and later `WinAPIGraph` will use it to generate the network.


# Install
	
`WinAPIGraph` uses py2neo to connect to the neo4j database, and Sqlite3 
for communication with the deviare2_db database.

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install py2neo.

```bash
pip install py2neo
```

## Usage

```bash
python3 WinAPIGraph.py
```
```
---------------------------------
Usage
---------------------------------

Options:
    -h, --help show brief help"
    -f, --file=PATH  specify the path of the file of the logs

```

![alt text](/docs/media/WinAPI.png?style=centerme)


# Starting a Graph

`WinAPIGraph` starts a VM through PyREBox, once all the malware analysis is executed 
and the VM is closed the process of network creation will start, for this it is necessary 
to have the neo4j database active. The script can be started through ``PyRLogToGraph.sh``.

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
```bash
./PyRLogToGraph.sh -p  /Your/path/malware.zip -m malware.exe

./PyRLogToGraph.sh -p /Your/path/malware.zip -m malware.exe -l /Your/path/function_calls.log
```


`WinAPIGraph` can also be run separately by simply entering the address where 
the log is located, from which we want to generate the network.

```bash
python3 WinAPIGraph.py -f /Your/path/function_calls.log
```

We start the process and obtain the resulting network


![alt text](/docs/media/graph.png?style=centerme)


## License
This tool is published under the [GNU GPLv3](LICENSE) license.

