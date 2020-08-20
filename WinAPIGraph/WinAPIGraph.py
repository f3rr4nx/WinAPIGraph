#!/usr/bin/env bash
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


from py2neo import Graph,Node,Relationship,database
import ast
import os
import configparser
import argparse
import os.path as path
import Api_db

# Global Variables
list_functions=[]
id_functions=0
pid=0
    

""" 
    Connects and authenticates with the neo4j database 
        bolt://localhost:7687
        auth=("name","password")
"""
def authenticateAndConnect():
    config = configparser.ConfigParser()        
    config.read('config.ini')
    connection = config['Neo4j']['connection']
    user = config['Neo4j']['user']
    passw = config['Neo4j']['pass']
    return Graph(connection, auth=(user, passw))

"""  
    Functions for creating nodes and relationships between them in the network 
    
        Create node whith a name (label) and arguments (properties)
            node = Node(*labels, **properties)
            graph.create(node)
    
        Create node Relatinship whith a name of the first node (start_node) 
        the name of the relationship (types) the name second node (end_node) 
        and the  arguments (properties)
            graph.create(Relationship(start_node, types, end_node, **properties))
"""
def Create_Node(labels, properties):
    node = Node(*labels, **properties)
    graph.create(node)
    return node

def Create_Relationship(start_node,end_node, types, properties):
    graph.create(Relationship(start_node, types, end_node, **properties))

""" 
    Converts the arguments of a specific function of the log, 
    so that they can be processed by neo4j. For example that 
    the ("\") does not detect by neo4j and proceeds to change them to ("/")
""" 
def Arguments(name,args):

    properties = {'name':name}
    for arg in args:
        if '\\' in arg:
            sent_str = arg.split('\\')
            arg=""
            for i in sent_str:
                arg += str(i) + "/"
            arg = arg[:-2]
        Arguments_name,Arguments_value = arg.split(': ')
        properties[Arguments_name] = Arguments_value
        properties['PiD'] = pid

    return properties

""" 
    Converts ONE arguments of a specific function of the log, 
    so that they can be processed by neo4j. For example that 
    the ("\") does not detect by neo4j and proceeds to change them to ("/")
    
        name_arg = if you want to rename the argument, this option allows you to do so, 
        but the original name of the argument is used by default
""" 
def One_Arguments(name,args,one_arg,name_arg=None):

    for arg in args:
        if '\\' in arg:
            sent_str = arg.split('\\')
            arg=""
            for i in sent_str:
                arg += str(i) + "/"
            arg = arg[:-2]
        if one_arg in arg:
            Arguments_name,Arguments_value = arg.split(": ")
    properties = {'name':name + "_" + Arguments_value}
    if(name_arg==None):
        properties[Arguments_name] = Arguments_value
    else:
        properties[name_arg] = Arguments_value
    properties['PiD'] = pid
    return properties
""" 
    Converts the arguments value of a specific function of the log, 
    so that they can be processed by neo4j. For example that 
    the ("\") does not detect by neo4j and proceeds to change them to ("/")
""" 
def argumen_value(name, args):
    for arg in args:
        if '\\' in arg:
            sent_str = arg.split('\\')
            arg=""
            for i in sent_str:
                arg += str(i) + "/"
            arg = arg[:-2]
        if name in arg:
            Arguments_name,Arguments_value = arg.split(": ")

    return Arguments_value


class Type_Func():
    """ The `Type_Func` class represents the way to create 
    the graph within a Neo4j database. The py2neo library is used 
    to connect and generate the graph.

    The argument `type_func` allows to process the function that has been obtained 
    from the log to be able to create the networks with `Type_Create` and `Type_Open` 
    and in this way to be able to standardize the process so that it is necessary 
    to be able to update it in a simpler way

        >>> from py2neo import Graph
        >>> Function = Type_Func(api,func, lista_args)
        >>> Function.type_func()


    The `Type_Create` argument allows a new node to be created in a graphics database.
    Nodes belonging to functions such as CreateFileA are only created once, 
    since these in turn generate a second node called File (in this example) 
    where all the information of the created file is found. 
    It checks if the function node already exists, if not it creates it and it generates 
    the secondary node with all the important information. As well as it generates 
    a relation between them.

        >>> from py2neo import Graph
        >>> Function = Type_Func(api,func, lista_args)
        >>> Function.type_func()

        >>> Function.Type_Create(self,name_func,name_api,labels_API,
            labels,name_labels,Type_Rel,Arg,name_arg)

     The full set of supported `settings` are:

    ===================  ========================================================  ==============  =========================  ==============
    Keyword              Description                                               Type            Example                    Default
    ===================  ========================================================  ==============  =========================  ==============
    ``name_func``        Use a specific URI scheme                                 str             ``'CreateFileA'``                 
    ``name_api``         Use a secure connection (TLS)                             str            ``kernel32``
    ``labels_API``       Verify the server certificate (if secure)                 str            ``True``
    ``labels``           Database server host name                                 str             ``'localhost'``
    ``name_labels``      Database server port                                      str             ``7687``
    ``Type_Rel``         Colon-separated host and port string                      str             ``'localhost:7687'``
    ``Arg``              User to authenticate as                                   str             ``'neo4j'``
    ``name_arg``         Password to use for authentication                        str             ``'password'``             ``'Handle'``
    ===================  ========================================================  ==============  =========================  ==============


    The `Type_Open` argument allows a new node to be created in a graphics database.
    But unlike `Type_Create` this node has an intermediate node because the system uses a buffer, 
    handler or other type of system to store data such as the size of the file.
    This data is of interest to save because this way you can see better than data accessed directly.
    It checks whether the function node already exists, if it does not. 
    Then it generates the intermediate node and finally the end node with all the important information. 
    In the case of ReadFile it would generate an intermediate node with the buffer and then join the file that has been created with `Type_Create`. 

        >>> from py2neo import Graph
        >>> Function = Type_Func(api,func, lista_args)
        >>> Function.type_func()

        >>> Function.Type_Open(self,name_func,name_api,labels_Api,labels_Node_1,
            labels_Node_2,name_node_1,name_node_2,Type_Rel,Arg_Node_1,Arg_Node_2,name_arg)

    The full set of supported `settings` are:

    ===================  ========================================================  ==============  =========================  ==============
    Keyword              Description                                               Type            Example                    Default
    ===================  ========================================================  ==============  =========================  ==============
    ``name_func``        Use a specific URI scheme                                 str             ``'CreateFileA'``                 
    ``name_api``         Use a secure connection (TLS)                             str            ``kernel32``
    ``labels_Api``       Verify the server certificate (if secure)                 str            ``True``
    ``labels_Node_1``    Database server host name                                 str             ``'localhost'``
    ``labels_Node_2``    Database server host name                                 str             ``'localhost'``
    ``name_node_1``      Database server port                                      str             ``7687``
    ``name_node_2``      Database server port                                      str             ``7687``
    ``Type_Rel``         Colon-separated host and port string                      str             ``'localhost:7687'``
    ``Arg_Node_1``       User to authenticate as                                   str             ``'neo4j'``
    ``Arg_Node_2``       User to authenticate as                                   str             ``'neo4j'``
    ``name_arg``         Password to use for authentication                        str             ``'password'``             ``'Handle'``
    ===================  ========================================================  ==============  =========================  ==============
   
    """
    def __init__(self, api, func, args):
        self.api=api
        self.func=func
        self.args = args

    def Type_Create(self,name_func,name_api,labels_API,labels,name_labels,Type_Rel,Arg,name_arg):
        global id_functions
        if str(self.func) in list_functions:
            a = Node(name_api, name=name_func)
            # Define a dictionary
            properties = One_Arguments(name_labels,self.args,Arg,name_arg)
            # Create Node
            b = Create_Node(labels , properties)

            properties = Arguments(name_labels,self.args)
            
            z = graph.nodes.match(name_api,name=name_func).first()
            types = Type_Rel + str(id_functions)
            Create_Relationship(z,b,types,properties)
        else:
            list_functions.append(self.func)
            # Define a dictionary
            properties = {'name': self.func}
            properties['PiD'] = pid
            # Create Node
            a = Create_Node(labels_API, properties)

            # Define a dictionary
            properties = One_Arguments(name_labels,self.args,Arg,name_arg)
            # Create Node
            b = Create_Node(labels, properties)
            properties = Arguments(name_labels,self.args)
            types = Type_Rel + str(id_functions)
            Create_Relationship(a,b,types,properties)
        id_functions += id_functions + 1
    
    def Type_Open(self,name_func,name_api,labels_Api,labels_Node_1,labels_Node_2,name_node_1,name_node_2,Type_Rel,Arg_Node_1,Arg_Node_2,name_arg):
        global id_functions
        if str(self.func) in list_functions:
            Arguments_value = argumen_value(Arg_Node_1,self.args)
            if(graph.nodes.match(name_node_1, Handle=Arguments_value).first()):
                properties = Arguments(name_node_1,self.args)
                a = graph.nodes.match(name_api, name=name_func).first()
                b = graph.nodes.match(name_node_1, Handle=Arguments_value).first()
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)
            else:
                # Define a list of labels
                # labels = [ 'Buffer' ]
                # Define a dictionary
                properties = One_Arguments(name_node_1,self.args,Arg_Node_1,name_arg)
                # Create Node
                b = Create_Node(labels_Node_1, properties)

                a = graph.nodes.match(name_api, name=name_func).first()
                
                properties = Arguments(name_node_1,self.args)
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)  
            Arguments_value = argumen_value(Arg_Node_2,self.args)
            if(graph.nodes.match(name_node_2, Handle=Arguments_value).first()):
                properties = Arguments(name_node_2,self.args)
                b = graph.nodes.match(name_node_2, Handle=Arguments_value).first()
                Arguments_value = argumen_value(Arg_Node_1,self.args)
                a = graph.nodes.match(name_node_1, Handle=Arguments_value).first()
                
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)
            else:
                # Define a list of labels
                # labels = [ 'File' ]
                # Define a dictionary
                properties = One_Arguments(name_node_2,self.args,Arg_Node_2,name_arg)
                # Create Node
                b = Create_Node(labels_Node_2, properties)

                Arguments_value = argumen_value(Arg_Node_1,self.args)
                a = graph.nodes.match(name_node_1, Handle=Arguments_value).first()
                
                properties = Arguments(name_node_1,self.args)
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)  
        else:
            list_functions.append(self.func)
            # Define a dictionary
            properties = {'name': self.func}
            properties['PiD'] = pid
            # Create Node
            a = Create_Node(labels_Api, properties)

            Arguments_value = argumen_value(Arg_Node_1,self.args)
            if(graph.nodes.match(name_node_1, Handle=Arguments_value).first()):
                properties = Arguments(name_node_1,self.args)
                a = graph.nodes.match(name_api, name=name_func).first()
                b = graph.nodes.match(name_node_1, Handle=Arguments_value).first()
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)

            else:
                # Define a list of labels
                # labels = [ 'Buffer' ]
                # Define a dictionary
                properties = One_Arguments(name_node_1,self.args,Arg_Node_1,name_arg)
                # Create Node

                b = Create_Node(labels_Node_1, properties)

                a = graph.nodes.match(name_api, name=name_func).first()
                properties = Arguments(name_node_1,self.args)

                types = Type_Rel + str(id_functions)

                Create_Relationship(a,b,types,properties)
            
            Arguments_value = argumen_value(Arg_Node_2,self.args)
            Arguments_value = Arguments_value.rstrip('\n')
            if(graph.nodes.match(name_node_2, Handle=Arguments_value).first()):
                properties = Arguments(name_node_2,self.args)
                b = graph.nodes.match(name_node_2, Handle=Arguments_value).first()
                Arguments_value = argumen_value(Arg_Node_1,self.args)
                a = graph.nodes.match(name_node_1, Handle=Arguments_value).first()
                
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)
            else:
                # Define a list of labels
                # labels = [ 'File' ]
                # Define a dictionary
                properties = One_Arguments(name_node_2,self.args,Arg_Node_2,name_arg)
                # Create Node
                b = Create_Node(labels_Node_2, properties)
                Arguments_value = argumen_value(Arg_Node_1,self.args)
                a = graph.nodes.match(name_node_1, Handle=Arguments_value).first()

                properties = Arguments(name_node_1,self.args)
                types = Type_Rel + str(id_functions)
                Create_Relationship(a,b,types,properties)  
        id_functions += id_functions + 1
    
    def type_func(self):
        import configparser
        global id_functions

        conn = Api_db.Conect_db()
        var = Api_db.select_functions_by_priority(conn,self.api,self.func)
        if var is True:
            conn = Api_db.Conect_db()
            rows = Api_db.select_args_by_priority(conn,self.api,self.func)
            list_row = []
            for row in rows:
                list_row.append(row[0])
            list_row.append("RET")
            
            if ".dll" in self.api:
                name_api = self.api.replace(".dll","")
            elif ".exe" in self.api:
                name_api = self.api.replace(".exe","")
            else:
                name_api,extension = self.api.split(".")
            
            name_api_ini = name_api.lower() + ".ini"
            config = configparser.ConfigParser()
            
            config.read('config.ini')

            api_path = config['Apis']['file_api']
            if config.read(api_path + name_api_ini):
                sections = config.sections()
                if self.func in sections: 
                    if "name_node_relationship" in config[self.func]: 
                        name_node = config[self.func]['name_node']
                        handle = config[self.func]['handle']
                        if "/" in handle:
                            arg_func,handle = handle.split("/")
                        name_Relationship = config[self.func]['name_relationship']
                        name_node_relationship = config[self.func]['name_node_relationship']
                        handle_node_relationship = config[self.func]['handle_node_relationship']
                        if "/" in handle_node_relationship:
                            arg_func_rel,handle_node_relationship = handle_node_relationship.split("/")
                        labels_Api = [ name_api.lower() ]
                        labels_Node = [ name_node ]
                        labels_Node_relationship  = [ name_node_relationship ]
                        if handle in list_row or arg_func in list_row and handle_node_relationship in list_row or arg_func_rel in list_row:
                            self.Type_Open(self.func,name_api.lower(),labels_Api,labels_Node,labels_Node_relationship,name_node,name_node_relationship,name_Relationship,handle,handle_node_relationship,"Handle")
                        else:
                            print("La función " + self.func + " tiene un argumento incorrecto. (" + handle + ") o (" + handle_node_relationship + ")")
                    else:
                        name_node = config[self.func]['name_node']
                        handle = config[self.func]['handle']
                        name_Relationship = config[self.func]['name_relationship']
                        labels_Api = [ name_api.lower() ]
                        labels_Node = [ name_node ]
                        if handle in list_row:
                            self.Type_Create(self.func,name_api.lower(),labels_Api,labels_Node,name_node,name_Relationship,handle,"Handle")
                        else:
                            print("La función " + self.func + " tiene un argumento incorrecto. (" + handle + ")")
                else:
                    pass#("The function " + self.func + " is not available. Please make sure that it is induced into the system.")
            else:
                pass#print("The Api " + self.api + " is not available. Please make sure that it is induced into the system.")

        if not var:            
            pass#print("Didn't find any " + self.func + " function in the " + self.api + " api.")
        else:
            pass#print("Found several functions similar to " + self.func + " please enter one of them for the system to process.")
        
        
                    
class Read_File:
    """ The `Read_File` class represents the reading of the log 
     obtained by the Pyrebox malware monitor. This process could be 
     adapted to other software analysis tools.

    """
    def __init__(self, dir):
        self.dir=dir
    def read(self):
        lista_func_kernel=[]
        lista_args=[]
        with open(self.dir, 'r') as reader:
            for line in reader:
                if 'Process (PID:' in line:
                    global pid
                    line_r,pid=line.split(')')

                #Obtenemos la linea en la que esta el proceso obtenido
                elif '-->' in line :
                    line_r=line.split('-->')
                    api = line_r[1].replace("]",'').replace("[",'').replace(" ",'')
                    api, func = api.split(':')
                elif '[OUT]' in line:
                    num = len(line.split())
                    if(num == 3):
                        args_1,args_2,args_3 = line.split()
                    elif (num == 4):
                        arg_1,args_2,args_3,args_4 = line.split()
                    elif (num == 5):
                        arg_1,args_2,args_3,args_4,args_5 = line.split()
                    else:
                        if 3 == len(line.split(":")):
                            args_1,args_2,args_3 = line.split(":")
                            args_3 = args_2 + ";" + args_3 + ":"
                            args_3 = args_3.replace(" ","")
                            args_1,args_2 = args_1.split("]")
                        else:
                            pass

                    lista_args.append(args_2 + ' ' + args_3)
                    #functions += "," + args + ":" + args_3
                elif '[IN ]' in line:
                    num = len(line.split())
                    if(num == 4):
                        args_1,args_2,args_3,args_4 = line.split()
                        lista_args.append(args_3 + ' ' + args_4)
                    else:
                        pass
                    #functions += "," + args + ":" + args_3
                elif '(+' in line:
                    num = len(line.split(":"))
                    if(num == 2):
                        args_1,args_2 = line.split(":")
                        args_1,args_3 = args_1.split(">")
                        lista_args.append(args_3 + ':' + args_2)
                    else:
                        pass
                elif 'RET' in line:
                    num = len(line.split())
                    if(num == 5):
                        arg_1,args_2,args_3,args_4,args_5 = line.split()
                    else:
                        arg_1,args_2,args_3,args_4 = line.split()
                    #functions += "," + "RET" + ":" + args_4
                    
                    lista_args.append("RET: " + args_4)
                    
                    l = Type_Func(api,func, lista_args)
                    l.type_func()
                    lista_args.clear()
                else:
                    pass
        return(lista_func_kernel)


def banner():
    print("============================================================")
    print("||       \ \        / / | |                               ||")
    print("||        \ \  /\  / /__| | ___ ___  _ __ ___   ___       ||")
    print("||         \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \      ||")
    print("||          \  /\  /  __/ | (_| (_) | | | | | |  __/      ||")
    print("||           \/  \/ \___|_|\___\___/|_| |_| |_|\___|      ||")
    print("============================================================")

def menu():

    # metavar gives name to the expected value 
    # in error and help outputs

    parser = argparse.ArgumentParser()
    
    parser.add_argument('-f', '--file', required=False, help="File to use")

    args = parser.parse_args()

    if args.file:
        if path.exists(args.file):
            logs_api = Read_File(args.file)
            lista_func_kernel=logs_api.read()
        else:
            print("The fild" + args.file + "is not found")       
    else:
        print("You need to enter a file using -f, --file")
        


if __name__ == '__main__':
    
    graph = authenticateAndConnect()
    banner()
    menu()
    # dirFichero="/home/fernando/Escritorio/pyrebox/logs/Aliana_mod/function_calls.log"
    # fichero = Read_File(dirFichero)
    # lista_func_kernel=fichero.read()

    

