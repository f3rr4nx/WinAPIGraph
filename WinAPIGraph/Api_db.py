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

import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_args_by_priority(conn, priority_api,priority_func):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()

    cur.execute("SELECT Functions.id FROM Modules JOIN ModulesFuncs ON Modules.id = ModulesFuncs.ModId JOIN Functions ON Functions.id = ModulesFuncs.FuncId WHERE Modules.name LIKE ? And Functions.Name=?", ('%'+priority_api+'%',priority_func))
    rows = cur.fetchall()
    for row in rows:
        id = row[0]
    cur.execute("SELECT FunctionsArgs.name FROM FunctionsArgs WHERE FunctionsArgs.FuncId =?", (id,))
    rows = cur.fetchall()
    return rows
    



def select_functions_by_priority(conn, priority_api,priority_func):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    
    cur.execute("SELECT Modules.Name, Functions.Name FROM Modules JOIN ModulesFuncs ON Modules.id = ModulesFuncs.ModId JOIN Functions ON Functions.id = ModulesFuncs.FuncId WHERE Modules.name LIKE ? And Functions.Name=?", ('%'+priority_api+'%',priority_func))
    rows = cur.fetchall()
    
    if (rows):
        return True
    else:
        cur.execute("SELECT Modules.Name, Functions.Name FROM Modules JOIN ModulesFuncs ON Modules.id = ModulesFuncs.ModId JOIN Functions ON Functions.id = ModulesFuncs.FuncId WHERE Modules.name LIKE ? And Functions.Name LIKE ?", ('%'+priority_api+'%','%'+priority_func+'%'))
        rows = cur.fetchall()
        if (rows):
            return (rows)
        else:
            return False
    
    #return Id, dll, name_func



def select_all_tasks(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM Functions")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def Conect_db():
    database = r"/home/fernando/Escritorio/neo4j/pip_neo4j/ficheros_api/deviare2_db/deviare32_populated.sqlite"

    # create a database connection
    conn = create_connection(database)
    return conn

if __name__ == '__main__':
    conn = Conect_db()
    p = select_functions_by_priority(conn,"ntdll.dll","NtQueryInformationProcess")
    x = select_args_by_priority(conn,"ntdll.dll","NtQueryInformationProcess")
    if p is True:
        print("solo encontro uno")
    elif not p:
        print("no encontro ninguno")
    else:
        print("Encontro varios")
# Initialize API doc database. We need to initialize it in this thread (callback),
# because sqlite limits db access to 1 thread, and the rest of callbacks should be
# running on this same thread.
#conn = create_connection("~/Escritorio/pyrebox/mw_monitor/third_party/deviare2_db/deviare32_populated.sqlite")
#select_all_tasks(conn)

# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any CreateMutexA function in the kernel32.dll api.
# Didn't find any CreateMutexA function in the kernel32.dll api.
# Didn't find any OpenProcessToken function in the KERNELBASE.dll api.
# Didn't find any OpenProcessToken function in the KERNELBASE.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any GetProcAddress function in the kernel32.dll api.
# Didn't find any NtQueryInformationProcess function in the ntdll.dll api.
# Didn't find any NtQueryInformationProcess function in the ntdll.dll api.