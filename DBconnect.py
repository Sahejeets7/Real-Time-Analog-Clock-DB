
import mysql.connector

def create_table(username, pwd):
    check_for_table_query = "show tables;"
    create_table_query = '''CREATE TABLE time_zones (
                                    India VARCHAR(30) NOT NULL DEFAULT '',
                                    USA VARCHAR(30)  NOT NULL DEFAULT '',
                                    UK VARCHAR(30)  NOT NULL DEFAULT '',
                                    Australia VARCHAR(30)  NOT NULL DEFAULT ''
                                    );'''
    try:
        db = mysql.connector.connect(
            user=username, host='localhost', password=pwd, database='AnalogClockDB')
        print(db)
        cursor = db.cursor()
        cursor.execute(check_for_table_query)
        result = cursor.fetchall()
        # if table doesn't exist
        if len(result) == 0:
            try:
                cursor.execute(create_table_query)
                print("\N{THUMBS UP SIGN} Table Created Successfully!")
            except:
                db.rollback()
                print("Please, try again! Some error occurred")    
        else:
            print("\N{THUMBS DOWN SIGN} Table already exists!!")    
    except:
        db.rollback()
        print("DB Connection Error occured")
    finally:
        db.close()


create_table("root", "christmas")
