#Login page

# -- CREATE TABLE User_Items (
# -- 	user_id SERIAL PRIMARY KEY,
# -- 	user_login VARCHAR(30) NOT NULL UNIQUE,
# -- 	user_pass VARCHAR(30) NOT NULL,
# -- 	user_name VARCHAR(30) DEFAULT 'no name',
# -- 	user_phone VARCHAR(30) DEFAULT '0',
# -- 	user_email VARCHAR(30) DEFAULT '@',
# -- 	user_city VARCHAR(30) DEFAULT 'no info',
# -- 	latitude DECIMAL,
# -- 	longitude DECIMAL
# -- )

# -- SELECT * FROM User_Items

#imports
import psycopg2
import config

class UserItem: 
    def __init__(self, user_login, user_pass):
        self.login = user_login
        self.passw = user_pass

# Create several methods (save, delete, update) these methods will allow a 
# user to save, delete and update items from the User_items table. 


# connect to the database
   
    def manage_connection(self, query):
        global connection
        try:
            connection = psycopg2.connect(
                host= config.HOST,
                port = config.PORT,
                database=config.BASE,
                user=config.USER,
                password=config.DB_PASSWORD
            )
            with connection:
                with connection.cursor() as cursor:   #it will close the cursor automatically
                    if 'SELECT' in query:
                        print('SELECT')
                        cursor.execute(query)
                        result = cursor.fetchall()
                        return result
                    else:
                        print('INSERT')
                        cursor.execute(query)
                        connection.commit()
        except:
            pass
        finally:
             #it will close the connection automatically
            if connection != None:
                connection.close()   
        
        #save
    def newuser(self): #Add check if User name exist
        query = f'''
INSERT INTO User_Items (user_login, user_pass)
VALUES ('{self.login}','{self.passw}')'''
        self.manage_connection(query)

    def deleteuser(self):
        query = f'''
    DELETE FROM User_Items WHERE user_login = '{self.login}' AND user_pass = '{self.passw}';
    '''
        self.manage_connection(query)

    
    def update(self,user_id, parametr,value):
        table_dict = {2:'user_pass', 3:'user_name', 4:'user_phone', 5:'user_email',6:'user_city',7:'latitude',8:'longitude'}
        col_update = f"{table_dict[parametr]} = '{value}'"
        query = f'''
    UPDATE User_Items 
    SET {col_update}
    WHERE user_id = '{user_id}';
    '''
        self.manage_connection(query)
        
        
class UserManager:
# Create a Class Method called get_by_name that will return a single 
# item from the Users_Items table depending on it’s name, if an object 
# is not found (there is no item matching the name in the get_by_name method)
# return None.

# Create a Class Method called all_items which will return a list of all 
# the items from the Users_Items table.  
    @classmethod
    def get_user_id(cls, user_login):
        query = f'''
SELECT  user_id FROM User_Items
WHERE user_login = '{user_login}' '''
        res = cls.manage_connection(query)
        if len(res) == 0:
            return  None
        else:
            return res[0][0]
    
    @classmethod
    def check_new_login(cls, user_login):
        query = f'''
SELECT COUNT(user_id) FROM User_Items
WHERE user_login = '{user_login}' '''
        res = cls.manage_connection(query)
        return res[0][0] == 0
    
    @classmethod
    def check_user_passw(cls, user_id, user_passw):
        query = f'''
SELECT  user_pass FROM User_Items
WHERE user_id = '{user_id}' '''
        res = cls.manage_connection(query)
        return user_passw == res[0][0]
    
    @classmethod
    def get_user_log_passw(cls, user_id):
        query = f'''
SELECT  user_login, user_pass FROM User_Items
WHERE user_id = '{user_id}' '''
        res = cls.manage_connection(query)
        if len(res) == 0:
            return  None
        else:
            return res
           
    @classmethod
    def get_user_info(cls, user_id):
        query = f'''
SELECT  user_login, user_name, user_phone, user_email  FROM User_Items
WHERE user_id = '{user_id}' '''
        res = cls.manage_connection(query)
        if len(res) == 0:
            return  None
        else:
            return res
        
    # get_user_city_lat_long
    @classmethod
    def get_user_city_lat_long(cls, user_id):
        query = f'''
SELECT  user_city, latitude, longitude  FROM User_Items
WHERE user_id = '{user_id}' '''
        res = cls.manage_connection(query)
        if len(res) == 0:
            return  None
        else:
            return res
        
        
    @classmethod
    def get_all_users(cls):
        query = f'''
SELECT user_id, user_login, user_name, user_phone, user_email FROM User_Items
'''
        res = cls.manage_connection(query)
        if len(res) == 0:
            return  None
        else:
            return res
    
    @staticmethod
    def manage_connection(query):
        base = 'Users'
        try:
            connection = psycopg2.connect(
                host=config.HOST,
                port = config.PORT,
                database=config.BASE,
                user=config.USER,
                password=config.DB_PASSWORD
            )
            with connection:
                with connection.cursor() as cursor:   #it will close the cursor automatically
                    if 'SELECT' in query:
                        print('SELECT')
                        cursor.execute(query)
                        result = cursor.fetchall()
                        return result
                    else:
                        print('INSERT')
                        cursor.execute(query)
                        connection.commit()
        except:
            pass
        finally:
             #it will close the connection automatically
            if connection != None:
                connection.close()  
    


#Tests
# user1 = UserItem('Dmitry','1234')
# user1.newuser()

# user2 = UserItem('Dmitry2','1235')
# user2.newuser()
# user3 = UserItem('Dmitry3','12356')
# user3.newuser()

# res = MenuManager.get_user_info(1)
# print(res)
# res = MenuManager.get_all_users()
# print(res)

# res = MenuManager.get_user_id('Dmitry2')
# print(res)

# a = input("User name for update:")
# id = MenuManager.get_user_id(a)
# print(id)
# p = input("password:")
# #chek

# itemup = UserItem(a,p)
# itemup.update(id,3,"Ivan")

# res = MenuManager.check_user_passw(1,input("pass"))
# print(res)

# res = UserManager.check_new_login('Dmihutry2')
# print(res)


# res = UserManager.get_user_id('Dima1')
# print(res)