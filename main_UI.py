# Menu UI
from tkinter import *
from tkinter import messagebox
from PIL import ImageTk, Image

import time
from time import strftime
from datetime import datetime

import requests

import os

# our file
from login_manager import *
from weather_info import get_current_weather
from send_sms import *
import config

#Designing Main Screen

def main_account_screen():
    
    global user_login_info
    global main_screen
    main_screen = Tk()   # create a GUI window 
    main_screen.geometry("350x500") # set the configuration of GUI window 
    main_screen.title("Account Login") # set the title of GUI window
 
# create a Form label
      
    Label(text= 'Main Menu', bg="lightgreen", width="300", height="2", font=("Calibri", 13)).pack() 
# add name if login
    if log_status:
        name_user = user_login_info[1] 
        Label(text=f'Hello {name_user}', font='Times 20', fg='grey').pack()
        Label(text="").pack()
    # create additional info
        Button(text="Send SMS", height="2", width="30",command=send_sms_to_id).pack() 
        Label(text="").pack() 
    
    # create  Update profile
        Button(text="Update profile info (U)", height="2", width="30",command = update).pack() 
        Label(text="").pack()     
    
    # create  Delete user
        Button(text="Delete user (D)", height="2", width="30",command = user_delete).pack() 
        Label(text="").pack()  
    
    # create  Log Out
        Button(text="Log Out (O)", height="2", width="30", command = logout).pack() 
        Label(text="").pack()  
        
                  
    else:
        Label(text="").pack() 
        Label(text="").pack() 
    # create a Login button
        Button(text="Login (L)", height="2", width="30", command = login).pack() 
        Label(text="").pack() 
    
    # create a Register button
        Button(text="Register new user (R)", height="2", width="30",command = register).pack() 
        Label(text="").pack() 
        main_screen.update()
        
  
# create a View basic info button
    Button(text="View Weather", height="2", width="30",command = lambda : weather_app('Tel Aviv')).pack() 
    Label(text="").pack() 
    
# create a Exit button
    Button(text="Exit (Q,E)", height="2", width="30",command=main_screen.destroy).pack() 
    Label(text="").pack() 
          
    main_screen.mainloop() # start the GUI

def register():
# The Toplevel widget work pretty much like Frame,
# but it is displayed in a separate, top-level window. 
#Such windows usually have title bars, borders, and other “window decorations”.
# And in argument we have to pass global screen variable
    
    global register_screen
    
    register_screen = Toplevel(main_screen) 
    register_screen.title("Register")
    register_screen.geometry("300x250")
    
     
# set global variables
    global username
    global password
    global username_entry
    global password_entry
 
# Set text variables
    username = StringVar()
    password = StringVar()
 
# Set label for user's instruction
    Label(register_screen, text="Please enter details below", bg="lightgreen").pack()
    Label(register_screen, text="").pack()
    
# Set username label
    username_lable = Label(register_screen, text="Username * ")
    username_lable.pack()
 
# Set username entry
# The Entry widget is a standard Tkinter widget used to enter or display a single line of text.
    
    username_entry = Entry(register_screen, textvariable=username)
    username_entry.pack()
   
# Set password label
    password_lable = Label(register_screen, text="Password * ")
    password_lable.pack()
    
# Set password entry
    password_entry = Entry(register_screen, textvariable=password, show='*')
    password_entry.pack()
    
    Label(register_screen, text="").pack()
    
# Set register button
    Button(register_screen, text="Register", width=10, height=1, bg="lightgreen", command = register_user).pack()
    Label(register_screen, text="").pack()
    Button(register_screen, text="Close", width=10, height=1, command=register_screen.destroy).pack() 

#Assigning Functions To Register Button
def register_user():
 
# get username and password
    username_info = username.get()
    password_info = password.get()
    
    log = username_info.strip()
    # check if login doesn't exist
    if UserManager.check_new_login(log): #if this login doesn't exist
        pas = password_info.strip()
        user_new = UserItem(log,pas)
        user_new.newuser()
        new_id = UserManager.get_user_id(log) 
        if new_id != None: #check if new info in table
            # print(f'New user with login: {log} and ID {new_id}\nUpdate your progile.')
            registration_sucess(log, new_id) #show if login is OK

        else:
            print(f'''Problem, try again''')
            # registration_error()
    else:
        # print(f'''User login =  {log} already exist. Try new one.''')
        login_exist(log)
 
    username_entry.delete(0, END)
    password_entry.delete(0, END)

def registration_sucess(log, new_id):
    global registration_success_screen
    global register_screen
    registration_success_screen = Toplevel(register_screen)
    registration_success_screen.title(f"Registration")
    registration_success_screen.geometry("200x200")
    Label(registration_success_screen,text="").pack()
    Label(registration_success_screen, text=f"New user with login: {log} \nand ID {new_id}.").pack()
    Label(registration_success_screen, text=f"Login and Update your progile.").pack()
    Label(registration_success_screen,text="").pack()
    Button(registration_success_screen, text="OK", command=delete_registration_success).pack()
    

def registration_error():
    global registration_error_screen
    registration_error_screen = Toplevel(register_screen)
    registration_error_screen.title("Error")
    registration_error_screen.geometry("150x100")
    Label(registration_error_screen, text="Registration Error").pack()
    Button(registration_error_screen, text="OK", command=delete_registration_error_screen).pack()
 
# Designing popup for user not found
 
def login_exist(log):
    global login_exist_screen
    login_exist_screen = Toplevel(register_screen)
    login_exist_screen.title("Registration")
    login_exist_screen.geometry("200x100")
    Label(login_exist_screen, text="").pack()
    Label(login_exist_screen, text=f"User login =  {log} already exist.").pack()
    Label(login_exist_screen, text=f"Try new one.").pack()
    Button(login_exist_screen, text="OK", command=delete_login_exist_screen).pack()
    

def delete_registration_success():
    registration_success_screen.destroy()
    register_screen.destroy()

def delete_registration_error_screen():
    registration_error_screen.destroy()
 
def delete_login_exist_screen():
    login_exist_screen.destroy()

# define login function
def login():
    
    global login_screen
    login_screen = Toplevel(main_screen)
    login_screen.title("Login")
    login_screen.geometry("300x250")
    Label(login_screen, text="Please enter details below to login").pack()
    Label(login_screen, text="").pack()
 
    global username_verify
    global password_verify
 
    username_verify = StringVar()
    password_verify = StringVar()
    
    global username_login_entry
    global password_login_entry
    
   
    Label(login_screen, text="Username * ").pack()
    username_login_entry = Entry(login_screen, textvariable=username_verify)
    username_login_entry.pack()
    Label(login_screen, text="").pack()
    
    
    Label(login_screen, text="Password * ").pack()
    password_login_entry = Entry(login_screen, textvariable=password_verify, show= '*')
    password_login_entry.pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Login", width=10, height=1, command=login_verification).pack()
    Label(login_screen, text="").pack()
    Button(login_screen, text="Close", width=10, height=1, command=login_screen.destroy).pack()
    
def login_verification():
    
    global user_login_info 
#get username and password
    username1 = username_verify.get()
    password1 = password_verify.get()
# this will delete the entry after login button is pressed
    username_login_entry.delete(0, END)
    password_login_entry.delete(0, END)
 
# #The method listdir() returns a list containing the names of the entries in the directory given by path.
#     list_of_files = os.listdir()  
#check login
    log = username1.strip()
    check_id_before = UserManager.get_user_id(log)
#defining verification's conditions 
    if check_id_before != None: #if this login exist:
        print("Ok")
        # file1 = open(username1, "r")   # open the file in read mode
        pas = password1.strip()
        if UserManager.check_user_passw(check_id_before, pas):
            status = True
            user_info = UserManager.get_user_info(check_id_before)[0]
            user_name_menu = user_info[1] if (user_info[1] != "no name" and user_info[1] != "")else user_info[0]
            user_login_info = status, user_name_menu, check_id_before, pas #for tests
            # print(user_login_info)
            login_sucess() #show if login is OK
 
        else:
            password_not_recognised()
 
    else:
        user_not_found()
 
# Designing popup for login success

def login_sucess():
    global login_success_screen
    global login_screen
    login_success_screen = Toplevel(login_screen)
    login_success_screen.title(f"login")
    login_success_screen.geometry("200x100")
    Label(text="").pack()
    Label(login_success_screen, text=f"You login as {user_login_info[1]}\nID is {user_login_info[2]}").pack()
    Button(login_success_screen, text="OK", command=delete_login_success).pack()
    
    

# Designing popup for login invalid password
 
def password_not_recognised():
    global password_not_recog_screen
    password_not_recog_screen = Toplevel(login_screen)
    password_not_recog_screen.title("Error")
    password_not_recog_screen.geometry("150x100")
    Label(password_not_recog_screen, text="Invalid Password ").pack()
    Button(password_not_recog_screen, text="OK", command=delete_login_password_not_recognised).pack()
 
# Designing popup for user not found
 
def user_not_found():
    global user_not_found_screen
    user_not_found_screen = Toplevel(login_screen)
    user_not_found_screen.title("Success")
    user_not_found_screen.geometry("150x100")
    Label(user_not_found_screen, text="Not Login").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_not_found_screen).pack()
 
    

# Deleting popups
def delete_login_success():
    login_success_screen.destroy()
    login_screen.destroy()
    global log_status 
    log_status  = True
    global main_screen
    main_screen.destroy()
    main_account_screen()
    
def delete_login_password_not_recognised():
    password_not_recog_screen.destroy()
 
def delete_user_not_found_screen():
    user_not_found_screen.destroy()
   
# Logic -------
def logout():
    # global login
    global log_status 
    log_status  = False
    global main_screen
    main_screen.destroy()
    main_account_screen()
    user_login_info = ()

# define delete function
def user_delete():
    
    global delete_screen
    delete_screen = Toplevel(main_screen)
    delete_screen.title("Delete")
    delete_screen.geometry("300x250")
    Label(delete_screen, text="").pack()
    Label(delete_screen, text="Enter details below to delete").pack()
    Label(delete_screen, text="").pack()
 
    # global username_verify
    global password2_verify
 
    # username_verify = StringVar()
    password2_verify = StringVar()
    
    # global username_login_entry
    global password_delete_entry
    
   
    # Label(login_screen, text="Username * ").pack()
    # username_login_entry = Entry(login_screen, textvariable=username_verify)
    # username_login_entry.pack()
    # Label(login_screen, text="").pack()
    
    
    Label(delete_screen, text="Password * ").pack()
    password_delete_entry = Entry(delete_screen, textvariable=password2_verify, show= '*')
    password_delete_entry.pack()
    Label(delete_screen, text="").pack()
    Button(delete_screen, text="Delete", width=10, height=1, command = lambda : user_delete_verification(user_login_info[2])).pack() #without lambda it's start comand by auto
    Label(delete_screen, text="").pack()
    Button(delete_screen, text="Close", width=10, height=1, command = delete_screen.destroy).pack()
    
def user_delete_verification(user_id):
    # print("WE WILL CHECK PASS")
    global user_login_info 
#get username and password
    # username1 = username_verify.get()
    password2 = password2_verify.get()
# this will delete the entry after login button is pressed
    # username_login_entry.delete(0, END)
    password_delete_entry.delete(0, END)
 

    pas = password2.strip()
    if UserManager.check_user_passw(user_id, pas):
        check_info = UserManager.get_user_log_passw(user_id)
        # print(check_info, user_id )
        if check_info != None:
            n = check_info[0][0]
            p = check_info[0][1]
            user_del = UserItem(n,p)
            user_del.deleteuser()
            #check if user_id exist???
            user_delete_sucess()
        else:
            # print("Base erroe")
            user_delete_not_found()
    else:
        delete_password_not_recognised()
 
# Designing popup for login success

def user_delete_sucess():
    global user_delete_success_screen
    global delete_screen
    user_delete_success_screen = Toplevel(delete_screen)
    user_delete_success_screen.title(f"Delete")
    user_delete_success_screen.geometry("200x100")
    Label(text="").pack()
    Label(user_delete_success_screen, text=f"User ID {user_login_info[2]}\n was Deleted").pack()
    Button(user_delete_success_screen, text="OK", command=delete_user_delete_success_screen).pack()
    
    

# # Designing popup for login invalid password
 
def delete_password_not_recognised():
    global delete_password_not_recog_screen
    global delete_screen
    delete_password_not_recog_screen = Toplevel(delete_screen)
    delete_password_not_recog_screen.title("Error")
    delete_password_not_recog_screen.geometry("150x100")
    Label(delete_password_not_recog_screen, text="Invalid Password ").pack()
    Button(delete_password_not_recog_screen, text="OK", command=delete_delete_password_not_recognised).pack()
 
# # Designing popup for user not found
 
def user_delete_not_found():
    global user_delete_not_found_screen
    ser_delete_not_found_screen = Toplevel(delete_screen)
    ser_delete_not_found_screen.title("Error")
    ser_delete_not_found_screen.geometry("150x100")
    Label(ser_delete_not_found_screen, text="Check user in database").pack()
    Button(user_not_found_screen, text="OK", command=delete_user_delete_not_found).pack()
 
    

# # Deleting popups
def delete_user_delete_success_screen():
    user_delete_success_screen.destroy()
    delete_screen.destroy()
    global log_status 
    log_status  = False
    global main_screen
    main_screen.destroy()
    main_account_screen()
    
def delete_delete_password_not_recognised():
    delete_password_not_recog_screen.destroy()
 
def delete_user_delete_not_found():
    user_delete_not_found_screen.destroy()

# update function
def update():
    global update_screen
    update_screen = Toplevel(main_screen)
    update_screen.title("Update")

    update_screen.geometry("600x300")
    update_screen.resizable(0, 0)

# configure the grid
    update_screen.columnconfigure(0, weight=1)
    update_screen.columnconfigure(1, weight=4)
    update_screen.columnconfigure(2, weight=4)
    update_screen.columnconfigure(3, weight=1)
# update_screen.columnconfigure(2, weight=4)

# Get info about profile: user_login, user_name, user_phone, user_email
    profile = UserManager.get_user_info(user_login_info[2])
    profile2 = UserManager.get_user_log_passw(user_login_info[2])
    profile3 = UserManager.get_user_city_lat_long(user_login_info[2]) #city, lat, long
    
    Label(update_screen, text=f"User profile ID: {user_login_info[2]}. Login: {profile2[0][0]}").grid(column=0, row=0, padx=5, pady=5)

 
    global update2_verify
    global update3_verify
    global update4_verify
    global update5_verify
 
    update2_verify = StringVar()
    update3_verify = StringVar()
    update4_verify = StringVar()
    update5_verify = StringVar()
    update6_verify = StringVar()
    
#     # global username_login_entry
#     # global password_login_entry

#Header
    Label(update_screen, text="Item").grid(column=0, row=1, padx=5, pady=5)
    Label(update_screen, text="Information").grid(column=1, row=1, padx=5, pady=5)
    Label(update_screen, text="New information").grid(column=2, row=1, padx=5, pady=5)

#1 row
    Label(update_screen, text="Password: ").grid(column=0, row=2, padx=5, pady=5)
    Label(update_screen, text=f"{profile2[0][1]}").grid(column=1, row=2, padx=5, pady=5)
    username_update_entry = Entry(update_screen, textvariable=update2_verify)
    username_update_entry.grid(column=2, row=2, padx=5, pady=5)
    Button(update_screen, text="Update", width=10, height=1, command = lambda : update_info_database(2, update2_verify)).grid(column=3, row=2, padx=5, pady=5)


#2 row
    Label(update_screen, text="Name: ").grid(column=0, row=3, padx=5, pady=5)
    Label(update_screen, text=f"{profile[0][1]}").grid(column=1, row=3, padx=5, pady=5)
    username_update_entry = Entry(update_screen, textvariable=update3_verify)
    username_update_entry.grid(column=2, row=3, padx=5, pady=5)
    Button(update_screen, text="Update", width=10, height=1, command = lambda : update_info_database(3, update3_verify)).grid(column=3, row=3, padx=5, pady=5)

#3 row
    Label(update_screen, text="Phone: ").grid(column=0, row=4, padx=5, pady=5)
    Label(update_screen, text=f"{profile[0][2]}").grid(column=1, row=4, padx=5, pady=5)
    username_update_entry = Entry(update_screen, textvariable=update4_verify)
    username_update_entry.grid(column=2, row=4, padx=5, pady=5)
    Button(update_screen, text="Update", width=10, height=1, command = lambda : update_info_database(4, update4_verify)).grid(column=3, row=4, padx=5, pady=5)

#4 row
    Label(update_screen, text="Email: ").grid(column=0, row=5, padx=5, pady=5)
    Label(update_screen, text=f"{profile[0][3]}").grid(column=1, row=5, padx=5, pady=5)
    username_update_entry = Entry(update_screen, textvariable=update5_verify)
    username_update_entry.grid(column=2, row=5, padx=5, pady=5)
    Button(update_screen, text="Update", width=10, height=1, command = lambda : update_info_database(5, update5_verify)).grid(column=3, row=5, padx=5, pady=5)

# 5 row
    Label(update_screen, text="City: ").grid(column=0, row=6, padx=5, pady=5)
    Label(update_screen, text=f"{profile3[0][0]}").grid(column=1, row=6, padx=5, pady=5)
    username_update_entry = Entry(update_screen, textvariable=update6_verify)
    username_update_entry.grid(column=2, row=6, padx=5, pady=5)
    Button(update_screen, text="Update", width=10, height=1, command = lambda : update_info_database(6, update6_verify)).grid(column=3, row=6, padx=5, pady=5)

# 6 row
    Button(update_screen, text="Close", width=15, height=2, command=update_screen.destroy).grid(column=0, row=7, columnspan = 4,  padx=5, pady=5)
    
    
def update_info_database(parametr1, parametr2):
    # print(user_login_info[2])
    # get
    value_update = parametr2.get()
    # print(value_update)
    value_update = value_update.strip()
    
    #check for city
    
    
    check_info = UserManager.get_user_log_passw(user_login_info[2])
    if check_info != None:
        n = check_info[0][0]
        p = check_info[0][1]
        user_update = UserItem(n,p)
        
        if parametr1 == 6:
            #check city and add lat - long
            data = get_latitude_longitude(value_update)
            if data != None:
                user_update.update(user_login_info[2], parametr1, value_update)
                user_update.update(user_login_info[2], 7, data[0])
                #update lat
                user_update.update(user_login_info[2], 8, data[1])
                #update long
                update_screen.destroy()
                update()
            else:
                messagebox.showinfo(""," City name not found or connection problem ")
                print('check city')
        else:
            user_update.update(user_login_info[2], parametr1, value_update)
            #refresh info
            update_screen.destroy()
            update()
    else:
        print("Problem with user check.")

def weather_app(city_start):
    print(city_start)
    
    weather_info = get_current_weather(city_start)
    #get qweather inf -> city = Tel Aviv -> city, weather,      
    # if OK from internet, else - manually + check connection
    
    #check if connection and data is OK
        #if yes draw interface - def weather screen
        #if NO draw no connection interface + update - def weather screen no connection
    # check = True
    # print(f"Weather in {city_name}:")
#     print(f"Temperature: {weather_info['temperature']}°C")
#     print(f"Humidity: {weather_info['humidity']}%")
#     print(f"Wind Speed: {weather_info['wind_speed']} m/s")
#     print(f"Description: {weather_info['description']}")
#     print(f"Pressure {weather_info['pressure']}")
    print(weather_info)
    
    if weather_info:
        city_in = city_start
        weather_in = weather_info['description'].upper()
        temp_in = int(float(weather_info['temperature']))
        hum_in = weather_info['humidity']
        pres_in = weather_info['pressure']
        win_in = weather_info['wind_speed']
        
        weather_screen_with_info(city_in, weather_in, temp_in, hum_in, pres_in, win_in)
    else:
        weather_screen_no_connection()
    
def weather_screen_with_info(city, weather, temp, hum, pres, win):
        try:    
            global weather_screen
            weather_screen = Toplevel(main_screen)
            weather_screen.title("weather")
            global dir_path 
            dir_path  = os.path.dirname(os.path.realpath(__file__))
            weather_screen.iconbitmap(dir_path+"\\Images\\" + 'icon.ico')
            weather_screen.geometry("800x400")
            weather_screen.resizable(0, 0)
    

   
            # #Body UI
            Frame(weather_screen,width = 800, height = 50, bg ='#353535').place(x=0,y=0)
            global img1
            #search bar
            img1 = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'search.png'))

            def on_enter(e):
                e1.delete(0, END)

            def on_leave(e):
                if e1.get()=='':
                    e1.insert(0,'Tel Aviv')

            global city_verify
 
            city_verify = StringVar()
            
            e1 = Entry(weather_screen,width=21,fg='black',bg='white',border=0, textvariable = city_verify)
            
            e1.config(font=('Calibry',12))

            e1.bind('<FocusIn>', on_enter)
            e1.bind('<FocusOut>', on_leave)
            e1.insert(0,'Tel Aviv')
            e1.place(x=550,y=15)

            #date
            a = datetime.today().strftime('%B')
            b = (a.upper())
            q = datetime.now().month
          
            now = datetime.now()
            c=now.strftime('%B')
            month= c[0:3]
  

            today = datetime.today()
            date = today.strftime('%d')

    #     # ct is city name
    #     def weather_city(ct):
    #         # Frame(width=500,height=50,bg='blue').place(x=0,y=0) #top left part
            l2 = Label(weather_screen,text=str(city),bg='#353535',fg='white') #city name
            l2.config(font=('Calibri',18))
            l2.place(x=20,y=8)
            
    #         city = ct
    #         query ='q=' + city
    #         # w_data=weather_data(query)
    #         # result = w_data
    #         # print(result)
    #         try:
    #             print("Check!")
    #             # check= '{}'.format(result['main']['temp'])
    #             # celsius='{}'.format(result['main']['temp'])
    #         except:
    #             messagebox.showinfo(""," City name not found ")

    #         c = 10 #(int(float(check)))
    #         # descp=("{}".format(result['wether'][0]['description']))
    #         weather = 'Clear' #("{}".format(result['wether'][0]['main']))
    #         print(weather)

    #         now = datetime.now()
    #         current_time = strftime("%H")

            global img

            if temp > 10 and ("HAZE" in weather or "CLEAR" in weather): #sunny
                Frame(weather_screen,width=800,height = 350, bg = '#f78954').place(x=0,y=50)
                img = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'sunny1.png'))
                Label(weather_screen,image=img,border=0).place(x=100,y=130)
                bcolor="#f78954"
                fcolor='white'

            elif temp > 10 and "CLOUDS" in weather: #Clouds
                Frame(weather_screen,width=800,height = 350, bg = '#7492b3').place(x=0,y=50)
                img = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'clouds1.png'))
                Label(weather_screen,image=img,border=0).place(x=100,y=130)
                bcolor="#7492b3"
                fcolor='white'

            elif "RAIN" in weather:
                Frame(weather_screen,width=800,height = 350, bg = '#60789e').place(x=0,y=50)
                img = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'rain1.png'))
                Label(weather_screen,image=img,border=0).place(x=100,y=130)
                bcolor="#60789e"
                fcolor='white'

            elif temp <= 10 and "FOG" in weather or "CLEAR" in weather:
                Frame(weather_screen,width=800,height = 350, bg = 'lightblue').place(x=0,y=50)
                img = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'sunny.png'))
                Label(weather_screen,image=img,border=0).place(x=100,y=130)
                bcolor="lightblue"
                fcolor='black'

            else:
                Frame(weather_screen,width=800,height = 350, bg = 'white').place(x=0,y=50)
                # img = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'search.png'))
                Ltext = Label(weather_screen,text=weather, bg = 'white', border=0)
                Ltext.place(x=70,y=180)
                Ltext.configure(font=('Calibri',23))
                bcolor="white"
                fcolor='black'
            
    #         # w_data= weather_data(query)
    #         # result= w_data

    #         e= 5 #("humidity:{}".format(result['main']['humidity']))
    #         f= 100#("presure:{}".format(result['main']['presure']))
    #         b1= 12#("Wind speed:{} m/s".format(result['main']['speed']))

            l5 = Label(weather_screen,text=str(month + " " + date),bg=bcolor,fg=fcolor)
            l5.configure(font=('Calibri',23))
            l5.place(x=330,y=335)

            l4= Label(weather_screen,text=str('Humidity '+str(hum)+"%"),bg=bcolor,fg=fcolor)
            l4.configure(font=('Calibri',11))
            l4.place(x=550,y=160)

            l4= Label(weather_screen,text=str('Presure '+str(pres)),bg=bcolor,fg=fcolor)
            l4.configure(font=('Calibri',11))
            l4.place(x=550,y=200)

            l4= Label(weather_screen,text=str('Wind '+str(win)+' m/s'),bg=bcolor,fg=fcolor)
            l4.configure(font=('Calibri',11))
            l4.place(x=550,y=240)

            l4= Label(weather_screen,text=str(str(temp) + " ℃"),bg=bcolor,fg=fcolor)
            l4.configure(font=('Calibri',50))
            l4.place(x=330,y=160)


    #     weather_city(ct='Tel Aviv')

    #     def cmd1():
    #         b = str(e1.get())
    #         weather_city(str(b))
    #         e1.delete(0, END)
    #         e1.insert(0,'Tel Aviv')
    #         e1.bind('<FocusIn>', on_enter)
            
            
            Button(weather_screen, image=img1,border=0, command = lambda: search_weather(city_verify)).place(x=750,y=14)
            Button(weather_screen, text=' Clsoe ', border=0, command=weather_screen_delete).place(x=730,y=360)
        
        except:
            weather_screen_no_connection()
            #pass

def weather_screen_no_connection():
     
    global weather_screen
    weather_screen = Toplevel(main_screen)
    weather_screen.title("weather")
    global dir_path 
    dir_path  = os.path.dirname(os.path.realpath(__file__))
    weather_screen.iconbitmap(dir_path+"\\Images\\" + 'icon.ico')
    weather_screen.geometry("800x400")
    weather_screen.resizable(0, 0)
    Frame(weather_screen,width = 800, height = 50, bg ='grey').place(x=0,y=0)
    Frame(weather_screen,width=800,height = 350, bg = 'white').place(x=0,y=50)
    global imgx
    imgx = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'error.png'))
    Label(weather_screen,image=imgx,border=0).place(x=200,y=50)
    global img1
        #search bar
    img1 = ImageTk.PhotoImage(Image.open(dir_path+"\\Images\\" + 'search.png'))

    def on_enter(e):
        e1.delete(0, END)

    def on_leave(e):
        if e1.get()=='':
            e1.insert(0,'Tel Aviv')
    
    global city_verify
    city_verify = StringVar()
    e1 = Entry(weather_screen,width=21,fg='black',bg='white',border=0,textvariable=city_verify)
    e1.config(font=('Calibry',12))
    
    e1.bind('<FocusIn>', on_enter)
    e1.bind('<FocusOut>', on_leave)
    e1.insert(0,'Tel Aviv')
    e1.place(x=550,y=15)
    #Buttons
    Button(weather_screen,image=img1,border=0,command=lambda : search_weather(city_verify)).place(x=750,y=14)
    Button(weather_screen,text=' Clsoe ',border=0,command=weather_screen_delete).place(x=730,y=360)


def search_weather(city):
    #get city from var
    city_update = city.get()
    city_update = city_update.strip()
    print(city_update)
    
    weather_info = get_current_weather(city_update)

    if weather_info != None:
        
    # if OK
        weather_screen.destroy()
        weather_app(weather_info['city_api'])
    #else show message:
    else:
        messagebox.showinfo(""," City name not found ")
    
    # try again
    
def weather_screen_delete():
    weather_screen.destroy()
   
# send sms

def send_sms_to_id():
    user_id = user_login_info[2]
    user_info_updated = UserManager.get_user_info(user_login_info[2])
    user_city_updated = UserManager.get_user_city_lat_long(user_login_info[2])
    
    # check ino and connection to database:
    if user_info_updated != None:
        phone = user_info_updated[0][2]
        # check phone number:
        if "+" not in phone or len(phone) < 7:
            messagebox.showinfo(""," Phone number not correct. Update profile. ")
        else:
            #check city info
            if user_city_updated != None:
                city_updated = user_city_updated[0][0]
                if city_updated != "no info":
                    send_weather_notifications(user_id)
                else:
                    messagebox.showinfo(""," City is not correct. Update profile. ")  
            else:
                messagebox.showinfo(""," Check conection or database City info ")   
    else:
        messagebox.showinfo(""," Check conection or database phone info ")
        #check phone number 



#Driver
global log_status
log_status = False
main_account_screen() # call the main_account_screen() function
