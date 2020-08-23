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

    select_statement = """SELECT FunctionsArgs.name FROM FunctionsArgs WHERE FunctionsArgs.FuncId in (SELECT Functions.id FROM Modules JOIN ModulesFuncs ON Modules.id = ModulesFuncs.ModId JOIN Functions ON Functions.id = ModulesFuncs.FuncId WHERE Modules.name LIKE '{}' And Functions.Name='{}')""".format('%'+priority_api+'%',priority_func)
    cur.execute(select_statement)
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



def Conect_db():
    database = r"/home/fernando/Escritorio/rep_prueba/WinAPIGraph/WinAPIGraph/API_Files/deviare2_db/deviare32_populated.sqlite"

    # create a database connection
    conn = create_connection(database)
    return conn

if __name__ == '__main__':
    conn = Conect_db()
    p = select_functions_by_priority(conn,"ntdll.dll","NtQueryInformation")
    x = select_args_by_priority(conn,"ntdll.dll","NtQueryInformationProcess")
    print(x)