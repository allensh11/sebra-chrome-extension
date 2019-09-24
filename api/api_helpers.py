import os, json, hashlib, jwt, datetime, mysql.connector
from flask import session
from libra_actions import account, balance, mint, transfer

class ApiHelper:
    def dbConn(self):
        config = {
            'host': 'db',
            'port': 3306,
            'database': 'sebra',
            'user': 'root',
            'password': 'e0N28ttq@%B',
            'charset': 'utf8',
            'use_unicode': True,
            'get_warnings': True,
        }
        ret = {}
        db = mysql.connector.Connect(**config)
        cursor = db.cursor()
        ret['db'] = db
        ret['cursor'] = cursor
        return ret

    def getUserById(self, userId, userType):
        dbObj = self.dbConn()
        cursor = dbObj['cursor']
        table = 'customers'
        if(userType == 'business'):
            table = 'businesses'
        cursor.execute("SELECT * FROM `"+table+"` WHERE id = " + userId)
        res = cursor.fetchall()
        for i in res:
            print(result.fetch_row())
        dbObj['db'].close()
        return None

    #Decode JWT token, check for validity
    def verifyToken(self, token, app):
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            return data
        except:
            return None

    def fields(self, cursor):
        results = {}
        column = 0
        for d in cursor.description:
            results[d[0]] = column
            column = column + 1
        return results

    def verifyUserByPassword(self, username, password, userType, app):
        dbObj = self.dbConn()
        cursor = dbObj['cursor']
        table = 'customers'
        if(userType == 'business'):
            table = 'businesses'
        cursor.execute("SELECT * FROM `"+table+"` WHERE username = '" + username + "' LIMIT 1" )
        res = cursor.fetchall()
        if(cursor.rowcount == 0):
            return json.dumps({'message': 'error', 'data': 'Not registered.'}), 401     
        userId = None
        mnemonic = None
        fieldMap = self.fields(cursor)
        for row in res:
            userId = row[fieldMap['id']]
            passStored = row[fieldMap['password']]
            mnemonic = row[fieldMap['mnemonic']]   
        dbObj['db'].close()
        passProvided = hashlib.md5(password.encode('utf-8')).hexdigest()
        if(passStored == passProvided and userId is not None and mnemonic is not None):
            session['userId'] = userId
            session['userType'] = userType
            ret = self.returnSuccessfulLogin(userId, mnemonic, userType, app)
            response = json.dumps({'message': 'success', 'data': ret})
            return response
        else:
            return json.dumps({'message': 'Not authorized'}), 401

    def returnSuccessfulLogin(self, userId, mnemonic, userType, app):
        ret = {}
        acc = account(mnemonic)
        ret['userId'] = userId
        ret['address'] = acc['address']
        ret['accountBalance'] = balance(acc['address'])
        ret['userType'] = userType
        tokenResp = jwt.encode({'user': userId, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)}, app.config['SECRET_KEY'])
        ret['token'] = tokenResp.decode('UTF-8')
        return ret

    def existingUserCheck(self, dbObj, userName, userType):
        table = 'customers'
        if(userType == 'business'):
            table = 'businesses'
        cursor = dbObj['cursor']
        cursor.execute("SELECT * FROM `"+table+"` WHERE username = '" + userName + "' LIMIT 1" )
        #test - but delete if diesnot work
        test = cursor.rowcount
        cursor.fetchall()
        return cursor.rowcount > 0

    def registerNewUser(self, dbObj, acc):
        table = 'customers'
        if(acc['userType'] == 'business'):
            table = 'businesses'
        cursor = dbObj['cursor']
        cursor.execute("INSERT INTO `"+table+"` (username, password, mnemonic, address) VALUES ('"+acc['username']+"', '"+acc['password']+"', '"+acc['mnemonic']+"', '"+acc['address']+"')" )
        if(cursor.rowcount > 0):
            dbObj['db'].commit()
            return cursor.lastrowid
        return None