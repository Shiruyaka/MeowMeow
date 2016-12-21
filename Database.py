import mysql.connector
import hashlib
from PyQt4 import QtGui, QtDeclarative, QtCore, QtDesigner, QtSvg, QtAssistant, Qt, QtDBus, QtHelp, QtTest, QtScript, QtNetwork, QtScriptTools, QtWebKit, QtXml, QtXmlPatterns

class Database(object):

    def __init__(self):
        try:

            database_connector = mysql.connector.connect(user='root', password='#OlciaKocia01', host='localhost', database='MeowMeowDb', port='3306')
        except Exception as e:
            print 'Cos sie popsulo'
            exit()



b = Database()
