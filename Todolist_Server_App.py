import socket
import json
import mysql.connector
from mysql.connector import Error


def createsocket():
    global s 
    s = socket.socket()
    print('Connection created')
    s.bind(('localhost', 9999))

    s.listen(5)
    print('Waiting for connections')

def getClient():
    while True:
        c, addr = s.accept()
        print('Connected with', addr)
        '''
        status = 'successful'
        message = 'signup is successful'
        resp = {
            "flag": status,
            "msg" : message
        }
        
        inputString = json.dumps(resp)
        c.send(inputString.encode())
        '''
        data = c.recv(1024).decode()
        parsed_data = json.loads(data)
        if parsed_data['flag'] == 'signup':
            print('signed up')
            signup(parsed_data, c)
        elif parsed_data['flag'] == 'login':
            print('logged in')
            login(parsed_data, c)
            
# For create account
def signup(data, c):
    cursor = connection.cursor()
    try:
        cursor.execute("""
                INSERT INTO User_Bio (first_name, last_name, email, gender, password)
                VALUES ( %s, %s, %s, %s, %s)
            """, ( data['fname'], data['lname'], data['mail'], data['gen'], data['password']))
        connection.commit()
        status = 'Account created'
        resp = {
            "check_status" : status
        }
        inputString = json.dumps(resp)
        c.send(inputString.encode())
        
    except Error as e:
        print(f'Error collecting details: {e}') 
        exit()    
            
    #For login
def login(data, c):
    cursor = connection.cursor()
    cursor.execute(f"""
            SELECT * FROM User_Bio WHERE email = %s AND password = %s
    """,(data['mail'], data['password'])
    )
    #Fetch's only one row
    row = cursor.fetchone()
    if row == None:
        # Send this to the client 
        status = 'Email or password is incorrect'
        resp = {
            "check_status": status
        }
        
        newLogged = json.dumps(resp)
        c.send(newLogged.encode())
        # Print on the server
        #print("Email or password is incorrect!")
        
    else:
        exit()
        
        
    
# Function to create a database connection
def create_connection():
        try:
            con = mysql.connector.connect(
                host="localhost",
                user="root",
                password="AAn123456$",
                database="ToDoList"
            )
            return con
        except Error as e: # Easy error handling
            print(f"Error connecting to MySQL: {e}")
            return None

def main():
    global connection
    connection = create_connection()
    if connection is None:
        return
        
    createsocket()
    getClient()
    connection.close()
    print("Goodbye!")

if __name__ == "__main__":
    main()
        
    