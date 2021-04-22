try:
    from Tkinter import Label, Menu, messagebox
    import Tkinter
except ImportError:
    from tkinter import Label, Menu, messagebox
    import tkinter as Tkinter

import math  # Required For Coordinates Calculation
import time  # Required For Time Handling
#
#
# class
#to store time in table with respect to the timezones
def get_time_zones():
    from datetime import datetime
    import pytz

    timeZ_india = pytz.timezone('Asia/Kolkata')
    timeZ_us = pytz.timezone('America/New_York')
    timeZ_uk = pytz.timezone('Europe/London')
    timeZ_aus = pytz.timezone('Australia/Sydney')

    dt_india = datetime.now(timeZ_india)
    t_ind = dt_india.strftime('%d %b %Y - %I:%M:%S %p')

    dt_us = datetime.now(timeZ_us)
    t_us = dt_us.strftime('%d %b %Y - %I:%M:%S %p')

    dt_uk = datetime.now(timeZ_uk)
    t_uk = dt_uk.strftime('%d %b %Y - %I:%M:%S %p')

    dt_aus = datetime.now(timeZ_aus)
    t_aus = dt_aus.strftime('%d %b %Y - %I:%M:%S %p')
    return t_ind, t_us, t_uk, t_aus

#to store the data in table using sql connectors
def save_db():
    import mysql.connector
    # check_for_table_query = "show tables;"
    # values = get_time_zones()

    # note - assumes table is already created
    insert_table_query = """INSERT INTO time_zones (India, USA, UK, Australia)
                            VALUES (%s,%s,%s,%s);"""
    try:
        db = mysql.connector.connect(user='root', host='localhost', password="christmas", database='AnalogClockDB')
        cursor = db.cursor()
        response = messagebox.askyesnocancel("Confirmation Popup",  "Are you sure you want to save current Time?")
        if response:
            try:
                values = get_time_zones() # convert current time to different timezones
                cursor.execute(insert_table_query, values)
                db.commit()
                print("Query Excecuted successfully - Inserted New Row for Current Time")
                # open popup on success
                messagebox.showinfo("Successful Popup",  "Saved Successfully!")
            except:
                db.rollback()
                messagebox.showwarning("Warning",  "Current Time couldn't be saved, Pls Try again!")
    except:
        db.rollback()
        print("Error occured")
        messagebox.showerror("Error",  "Current Time couldn't be saved, some error occured!")
    finally:
        cursor.close()
        db.close()


def populate_data(rows):
    my_w = Tkinter.Tk()
    my_w.geometry("1100x700")

    # columns headings of grid
    e = Label(my_w, padx=50, pady=6, width=1, text='ID', relief='raised',
              anchor='center', bg='Black', font=("Courier", 13), fg="white")
    e.grid(row=0, column=0)
    e = Label(my_w, padx=50, pady=6, width=15, text='India',
              relief='raised', anchor='center', bg='Black', font=("roboto", 13),fg="white")
    e.grid(row=0, column=1)
    e = Label(my_w, padx=50, pady=6, width=15, text='USA',
              relief='raised', anchor='center', bg='Black', font=("roboto", 13),fg="white")
    e.grid(row=0, column=2)
    e = Label(my_w, padx=50, pady=6, width=15, text='UK',
              relief='raised', anchor='center', bg='Black', font=("roboto", 13),fg="white")
    e.grid(row=0, column=3)
    e = Label(my_w, padx=50, pady=6, width=15, text='Australia',
              relief='raised', anchor='center', bg='Black', font=("roboto", 13),fg="white")
    e.grid(row=0, column=4)

    count = 1 # 0th row is for column headings
    # populating rows of grid
    for row in rows:
        # for id column
        e = Label(my_w, padx=50, pady=6, width=1, text=count,
                anchor="center", font=("roboto", 13),bg="#99ced3",fg="black", relief='sunken')
        e.grid(row=count, column=0,padx=2,pady=2)
        # for main data 
        for j in range(len(row)):
            e = Label(my_w, padx=50, pady=6, width=15,
                      text=row[j],anchor="center", font=("roboto", 13), bg="#99ced3",fg="black", relief='sunken')
            e.grid(row=count, column=j+1, padx=2,pady=2)
        count += 1
# fetch records from database and display normally in a grid fashion 
def show_db_normal():
    import mysql.connector

    check_for_table_query = "show tables;"
    select_from_table_query = "SELECT * FROM time_zones"
    try:
        db = mysql.connector.connect(
            user="root", host='localhost', password="christmas", database='AnalogClockDB')
        cursor = db.cursor()
        cursor.execute(check_for_table_query)
        result = cursor.fetchall()
        if len(result) == 0:
            print("No Table Found! Pls Create table first")
        else:
            cursor.execute(select_from_table_query)
            rows = cursor.fetchall()
            if len(rows) == 0:
                print("No Saved Time Records found! Please try saving some TimeZone records first")
                messagebox.showwarning("Warning",  "No Saved Time Records found! Please try saving some Times first")
            else:
                # looping over and populating in new tkinter window
                populate_data(rows)
                # show_db_treeview(rows)  # show data in treeview widget

    except:
        print("Error occured")
        messagebox.showerror("Error",  "some error occured!")
    finally:
        cursor.close()
        db.close()

#to create the sticks(clock hands)
class main(Tkinter.Tk):
    def __init__(self, x, y):
        Tkinter.Tk.__init__(self)
        self.x = x  # Center Point x
        self.y = y  # Center Point
        self.length = 50  # Stick Length
        self.creating_all_function_trigger()

    # Creating Trigger For Other Functions
    def creating_all_function_trigger(self):
        self.create_canvas_for_shapes()
        self.creating_background_()
        self.creating_sticks()
        return

    # Creating Background
    def creating_background_(self):
        self.image = Tkinter.PhotoImage(file='clock.gif')
        self.canvas.create_image(self.x, self.y, image=self.image)
        return

    # creating Canvas
    def create_canvas_for_shapes(self):
        self.canvas = Tkinter.Canvas(self)
        self.canvas.pack(expand='yes', fill='both')
        return

    # Creating Moving Sticks
    def creating_sticks(self):
        self.sticks = []
        for i in range(2):
            store = self.canvas.create_line(
                self.x, self.y, self.x+self.length, self.y+self.length, width=2.5, fill='tomato')
            self.sticks.append(store)
        seconds_hand = self.canvas.create_line(
            self.x, self.y, self.x+self.length, self.y+self.length, width=2, fill='teal')
        self.sticks.append(seconds_hand)
        return

    # Function Need Regular Update
    def update_class(self):
        now = time.localtime()
        t = time.strptime(str(now.tm_hour), "%H")
        hour = int(time.strftime("%I", t))*5
        now = (hour, now.tm_min, now.tm_sec)
        # Changing Stick Coordinates
        for n, i in enumerate(now):
            x, y = self.canvas.coords(self.sticks[n])[0:2]
            cr = [x, y]
            cr.append(self.length*math.cos(math.radians(i*6) - math.radians(90))+self.x)
            cr.append(self.length*math.sin(math.radians(i*6) - math.radians(90))+self.y)
            self.canvas.coords(self.sticks[n], tuple(cr))
        return

    def create_Buttons(self):
        lblfrstrow = Tkinter.Label(
            self, text="Press Button to Save current time", font=("Roboto", 16))
        lblfrstrow.place(x=90, y=250)
        # password = Tkinter.Entry(self, width=35)
        # password.place(x=170, y=250, width=200, height=30)
        # onclick will store time in db
        submitbtn = Tkinter.Button(
            self, text="Save", bg='seagreen', command=save_db)
        submitbtn.place(x=180, y=300, width=100, height=40)
        displaybtn = Tkinter.Button(
            self, text="Show Saved records", bg='#99ced3', command=show_db_normal)
        displaybtn.place(x=155, y=370, width=150, height=40)

    def create_menu(self):
        menubar = Menu(self, activebackground="red")
        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_separator()
        filemenu.add_command(label="Save Current Time")
        filemenu.add_separator()
        menubar.add_command(label="Exit", command=self.destroy)
        self.config(menu=menubar)
# Main Function Trigger
if __name__ == '__main__':
    root = main(225, 100)
    # clock2=main(100,100)
    root.title("analog clock")
    root.geometry("450x500")

    root.create_Buttons()
    root.create_menu()

    # Creating Main Loop
    while True:
        root.update()
        root.update_idletasks()
        root.update_class()
