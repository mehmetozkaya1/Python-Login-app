from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from smtplib import SMTP
import emailim

master = Tk()

class App(Tk):

    def __init__(self):

        master.title("Login")
        master.resizable(False,False)

        self.icon_img = PhotoImage(file="user-interface.png")
        master.iconphoto(False, self.icon_img)
        
        self.canvas = Canvas(master, width=1000,height=500)
        self.canvas.pack()

        # Image
        self.pic = Image.open("loginn.png")
        self.resized_pic = self.pic.resize((450, 450), Image.LANCZOS)
        self.resized_pic = ImageTk.PhotoImage(self.resized_pic)

        self.image_label = Label(master, image=self.resized_pic)
        self.image_label.place(x=35,y=25)

        # Frame

        self.frame = Frame(master, bg="white", width=450, height=450)
        self.frame.place(x=520,y=25)

        self.black_frame1 = Frame(self.frame, bg="black",height=3,width=280)
        self.black_frame1.place(x=80, y=140)

        self.black_frame2 = Frame(self.frame, bg="black",height=3,width=280)
        self.black_frame2.place(x=80, y=230)

        # Labels

        self.signin_label = Label(self.frame, text="Sign in",bg="white", font=("Microsoft YaHei UI Light",23,"bold"),fg="#57a1f8")
        self.signin_label.place(x=170, y=20)

        self.signup1_label = Label(self.frame, text="Don't you have an account?",fg="black",bg="white",font=("Microsoft YaHei UI Light",11))
        self.signup1_label.place(x=77, y=330)

        self.forget_label = Label(self.frame, text="Have you forgotten your password?",fg="black",bg="white",font=("Microsoft YaHei UI Light",11))
        self.forget_label.place(x=77, y=352)

        # Entries

        self.username_entry = Entry(self.frame,border=0 , width=23,font=("Microsoft YaHei UI Light",14))
        self.username_entry.place(x=80,y=110)
        self.username_entry.insert(0,"Username")
        self.username_entry.bind("<FocusIn>", self.on_enter_user)
        self.username_entry.bind("<FocusOut>", self.on_leave_user)

        self.password_entry = Entry(self.frame,border=0 , width=23,font=("Microsoft YaHei UI Light",14))
        self.password_entry.place(x=80,y=200)
        self.password_entry.insert(0,"Password")
        self.password_entry.bind("<FocusIn>", self.on_enter_pass)
        self.password_entry.bind("<FocusOut>", self.on_leave_pass)

        # Button

        self.signin_button = Button(self.frame,border=0 , width=23, font=("Microsoft YaHei UI Light",14,"bold"), fg="white" , bg="#57a1f8", text="Sign in",command=self.sign_in)
        self.signin_button.place(x=80, y=290)

        self.signup_button = Button(self.frame,border=0 ,cursor="hand2", font=("Microsoft YaHei UI Light",9), fg="#57a1f8" , bg="white", text="Sign up",command=self.sign_up_window)
        self.signup_button.place(x=270, y=331)

        self.click_button = Button(self.frame,border=0 ,cursor="hand2", font=("Microsoft YaHei UI Light",8), fg="#57a1f8" , bg="white", text="Click here",command=self.send_email)
        self.click_button.place(x=320, y=354)

    def on_enter_user(self,e):

        self.username_entry.delete(0, "end")

    def on_leave_user(self,e):

        self.name = self.username_entry.get()

        if self.name == "":

            self.username_entry.insert(0, "Username")
    
    def on_enter_pass(self,e):

        self.password_entry.delete(0, "end")

    def on_leave_pass(self,e):

        self.password = self.password_entry.get()

        if self.password == "":

            self.password_entry.insert(0, "Password")

    def connect_to_server(self):

        self.connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="*******",
            database="login-app"
        )

    def disconnet_from_server(self):

        self.connection.close()

    def create_cursor(self):

        self.cursor = self.connection.cursor()

    def sign_in(self):
        
        try:

            self.connect_to_server()
            self.create_cursor()

            self.username = self.username_entry.get()
            self.password = self.password_entry.get()

            self.find_user_sql = f"Select password from users where username='{self.username}'"
            self.cursor.execute(self.find_user_sql)
            self.user_password = self.cursor.fetchone()

            if self.password == self.user_password[0]:

                self.message = "Successfully logged in."
                messagebox.showinfo("Success!",self.message)

                master.destroy()

                secondary = Tk()
                secondary.title("Window")
                canvas = Canvas(secondary, height=500, width= 1000)
                canvas.pack()

                secondary_label = Label(secondary, font=("Microsoft YaHei UI Light",30,"bold"), fg="white" , bg="#57a1f8", text="Logged In\n\nGithub = github.com/mehmetozkaya1\n\nLinkedIn = linkedin.com/in/mehmetozkaya-")
                secondary_label.place(x=80,y=100)

                secondary.mainloop()
            
            else:
                
                self.message = "Failed to login. Please check your username and password."
                messagebox.showerror("Failed!",self.message)

        except:

            self.message = "Failed to login. Please check your username and password."
            messagebox.showerror("Failed!",self.message)

        finally:

            self.disconnet_from_server()
    
    def send_email(self):

        try:

            self.connect_to_server()
            self.create_cursor()

            self.email_username = self.username_entry.get()

            self.find_emailAndPassword_sql = f"Select email,password from users where username='{self.email_username}'"
            self.cursor.execute(self.find_emailAndPassword_sql)

            self.emailAndPassword = self.cursor.fetchone()
            self.sendTo_email = self.emailAndPassword[0]
            self.email_password = self.emailAndPassword[1]

            self.sender_email = emailim.my_email
            self.sender_password = emailim.password

            self.email_content = f"Your password is {self.email_password}."

            self.mail = SMTP("smtp.gmail.com", 587)
        
            self.mail.ehlo()
            self.mail.starttls()
            self.mail.login(self.sender_email,self.sender_password)
            self.mail.sendmail(self.sender_email, self.sendTo_email, self.email_content.encode("utf-8"))

            self.hidden_email = self.sendTo_email[0:3] + "*"*7 + self.sendTo_email[-10:]

            self.warning_message = f"We have sent you an e-mail to remind you the password. E-mail:\n\n{self.hidden_email}"
            messagebox.showinfo("Success!",self.warning_message)

        except:

            self.message = f"Failed to find the user with the username '{self.email_username}'"
            messagebox.showerror("Failed!",self.message)

    def sign_up_window(self):

        secondary = Tk()

        class SecondWindow(Tk):

            def __init__(self):

                secondary.title("Sign up")
                secondary.resizable(False,False)

                self.canvas2 = Canvas(secondary,width=450,height=500)
                self.canvas2.pack()

                self.frame2 = Frame(secondary, bg="white", width=400, height=465)
                self.frame2.place(x=25,y=20)

                self.signin_label = Label(self.frame2, text="Sign up",bg="white", font=("Microsoft YaHei UI Light",20,"bold"),fg="#57a1f8")
                self.signin_label.place(x=150, y=20)

                self.username_entry2 = Entry(self.frame2,border=0 , width=23,font=("Microsoft YaHei UI Light",14))
                self.username_entry2.place(x=71,y=110)
                self.username_entry2.insert(0,"Username")
                self.username_entry2.bind("<FocusIn>", self.on_enter_user2)
                self.username_entry2.bind("<FocusOut>", self.on_leave_user2)

                self.password_entry2 = Entry(self.frame2,border=0 , width=23,font=("Microsoft YaHei UI Light",14))
                self.password_entry2.place(x=71,y=180)
                self.password_entry2.insert(0,"Password")
                self.password_entry2.bind("<FocusIn>", self.on_enter_pass2)
                self.password_entry2.bind("<FocusOut>", self.on_leave_pass2)

                self.email_entry = Entry(self.frame2,border=0 , width=23,font=("Microsoft YaHei UI Light",14))
                self.email_entry.place(x=71,y=250)
                self.email_entry.insert(0,"E-mail")
                self.email_entry.bind("<FocusIn>", self.on_enter_email)
                self.email_entry.bind("<FocusOut>", self.on_leave_email)

                self.black_frame3 = Frame(self.frame2, bg="black",height=3,width=257)
                self.black_frame3.place(x=71, y=140)

                self.black_frame4 = Frame(self.frame2, bg="black",height=3,width=257)
                self.black_frame4.place(x=71, y=210)

                self.black_frame5 = Frame(self.frame2, bg="black",height=3,width=257)
                self.black_frame5.place(x=71, y=280)

                self.signup_button = Button(self.frame2,border=0 , width=21, font=("Microsoft YaHei UI Light",14,"bold"), fg="white" , bg="#57a1f8", text="Sign up",command=self.sign_up)
                self.signup_button.place(x=71, y=320)

            def get_usernames(self):

                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="******",
                    database="login-app"
                )

                self.cursor = self.connection.cursor()

                self.get_usernames_sql = "Select username from users"
                self.cursor.execute(self.get_usernames_sql)

                self.usernames_tuple = self.cursor.fetchall()
                self.usernames = []
                
                for i in range(len(self.usernames_tuple)):

                    self.usernames.append(self.usernames_tuple[i][0])

                self.connection.close()
            
            def sign_up(self):

                self.username2 = self.username_entry2.get()
                self.password2 = self.password_entry2.get()
                self.email = self.email_entry.get()

                if "@gmail.com" in self.email:

                    self.get_usernames()

                    if not self.username2 in self.usernames:

                        try:

                            self.connection = mysql.connector.connect(
                                host="localhost",
                                user="root",
                                password="********",
                                database="login-app"
                            )

                            self.cursor = self.connection.cursor()

                            self.sign_up_sql = "INSERT INTO users (username, password, email) VALUES(%s,%s,%s)"
                            self.sign_up_values = (self.username2, self.password2, self.email)

                            self.cursor.execute(self.sign_up_sql,self.sign_up_values)

                            self.connection.commit()
                            self.message = "You've successfully signed up."
                            messagebox.showinfo("Success!",self.message)
                            secondary.destroy()
                    
                        except:

                            self.message = "Failed to sign up."
                            messagebox.showerror("Failed!",self.message)
                    
                        finally:
                                
                            self.del_id_column()
                            self.add_id_column()
                            self.connection.close()

                    elif self.username2 in self.usernames:

                        self.message = f"There is an account with the username '{self.username2}'"
                        messagebox.showerror("Failed!",self.message)
                
                else:

                    self.message = "Please enter a valid e-mail address. E-mail address has to be a gmail address."
                    messagebox.showerror("Failed!",self.message)

            def on_enter_user2(self,e):

                self.username_entry2.delete(0, "end")

            def on_leave_user2(self,e):

                self.name2 = self.username_entry2.get()

                if self.name2 == "":

                    self.username_entry2.insert(0, "Username")
            
            def on_enter_pass2(self,e):

                self.password_entry2.delete(0, "end")

            def on_leave_pass2(self,e):

                self.password2 = self.password_entry2.get()

                if self.password2 == "":

                    self.password_entry2.insert(0, "Password")
            
            def on_enter_email(self,e):

                self.email_entry.delete(0, "end")

            def on_leave_email(self,e):

                self.email = self.email_entry.get()

                if self.email == "":

                    self.email_entry.insert(0, "E-mail")

            def add_id_column(self):

                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="********",
                    database="login-app"
                )

                self.cursor = self.connection.cursor()

                self.new_column_sql = "ALTER TABLE users \
                ADD id INT \
                AUTO_INCREMENT PRIMARY KEY \
                FIRST"

                self.cursor.execute(self.new_column_sql)

                self.connection.commit()

            def del_id_column(self):

                self.connection = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="***********",
                    database="login-app"
                )

                self.cursor = self.connection.cursor()

                self.new_column_sql = "ALTER TABLE users DROP COLUMN id"

                self.cursor.execute(self.new_column_sql)

                self.connection.commit()
                
        second = SecondWindow()
        secondary.mainloop()
            
login_app = App()
master.mainloop()