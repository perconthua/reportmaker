from collections import OrderedDict
import MySQLdb
from MySQLdb.cursors import DictCursor



def get_config():
    config = ConfigParser.ConfigParser()
    config.read('config.ini')
    return config

def connect():
    # config = get_config()
    # user = config.get("yachay2","user")
    # passwd = config.get("yachay2","passwd")
    # db = config.get("yachay2","db")
    # host = config.get("yachay2","host")

    user = "yachay"
    passwd = "123-surf"
    host = "161.132.8.42"
    db = "yachay2"
    
    # user = "operador"
    # passwd = "J6HXD58M5K"
    # host = "161.132.8.222"
    # db = "chavin"

    return MySQLdb.connect(host=host, user=user, passwd=passwd, db=db, cursorclass=DictCursor)


def sql(db,query,commit=False):
    cur = db.cursor() 
    cur.execute(query)
    if(commit):
        db.commit()
    
    # return cur.fetchall()
    # python shufles columns order

    r=cur.fetchall()
    ordercols = [i[0] for i in cur.description]
    
    result=[]
    for row in r:
        aux=OrderedDict()
        for col in ordercols:
            if hasattr(row[col],"decode"):
                aux[col]=row[col].decode('utf-8')
            else:
                aux[col]=row[col]
        result.append(aux)
    return result
