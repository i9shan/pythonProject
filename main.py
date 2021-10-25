import sqlite3
import xlrd
import pandas as pd
import csv
from glob import glob
from os.path import expanduser

connection = sqlite3.connect("user.db")

sheet = pd.read_excel('chyper-code.xlsx')
data = sheet['USER TYPE']
edata = sheet['SYSTEM CONVERT']
l=0
print("-----Welcome to Application---")
while l==0:
    u=str(input("Are you a new user?(Y/N)"))
    if u.upper() == 'Y':
        data = sheet['USER TYPE']
        edata = sheet['SYSTEM CONVERT']
        cursor = connection.cursor()
        login = str(input("Enter your login id :"))
        passw = str(input("Enter your password :"))
        login_query = "SELECT loginid FROM user WHERE loginid='" + login + "';"
        cursor.execute(login_query)
        user_results = cursor.fetchall()
        users = []
        for i in user_results:
            users.append(i[0])
        if login not in users:
            epass = ''
            i=0
            for j in passw:
                for i in range(0, 36):
                    if j.upper() == str(data[i]):
                        epass += str(edata[i])
            insert = """INSERT INTO user(loginid, password) VALUES ( ?, ?)"""
            data = (login, epass)
            cursor.execute(insert, data)
            print("Account created Successfully")
            cursor.execute("COMMIT;")

            cursor.close()
        else :
            print("Login id already exists")
        l = int(input("Enter 0 to continue"))
    elif u.upper() =='N':
        data = sheet['USER TYPE']
        edata = sheet['SYSTEM CONVERT']
        cursor = connection.cursor()
        login = str(input("Enter your login id :"))
        login_query="SELECT loginid FROM user WHERE loginid='" + login + "';"
        cursor.execute(login_query)
        user_results = cursor.fetchall()
        users=[]
        for i in user_results:
            users.append(i[0])
        query = "SELECT * FROM user WHERE loginid='" + login + "';"
        cursor.execute(query)
        results = cursor.fetchall()
        if login in users:
            passw = str(input("Enter your password : "))
            epass=''
            for j in passw:
                for i in range(0,36):
                    if j.upper() == str(data[i]):
                        epass += str(edata[i])
            if epass.upper() == results[0][2]:
                count = int(results[0][3])+1
                count = str(count)
                userid = str(results[0][0])
                updateQuery = "UPDATE user SET access_count='" + count + "'WHERE userid='" + userid + "';"
                cursor.execute(updateQuery)
                cursor.execute("COMMIT;")
                print("login Successful")
                print("User login:", results[0][1], " No of logins :", count)
                backup_query="SELECT * FROM user"
                cursor.execute(backup_query)
                backup_query_results = cursor.fetchall()
                clients = pd.read_sql('SELECT * FROM user', connection)
                clients.to_csv('userdb-backup.csv', index=False)
                l = int(input("Enter 0 to continue"))
                cursor.close()
            else :
                print("Invalid Password")
        else :
            print("Invalid Login ID")
    else :

        print("Invalid input")

cursor.close()
connection.close()