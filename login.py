import csv
from tkinter import *
from tkinter import messagebox
from database import db


class User:
    def __init__(self, user_id):
        if user_id == -1:
            self.username = None
            self.user_id = None
        else:
            result = db.getinfo(user_id)
            self.username = result[0][1]
            self.user_id = user_id


class UserFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.welcome_msg = StringVar(parent)
        Label(self, textvariable=self.welcome_msg).grid(row=1, column=0, sticky='NW')
        Button(self, text="Logout", command=self.logout).grid(row=1, column=1, sticky='NE')
        self.content = StringVar()
        Button(self, text="New AD", command=self.ad).grid(row=1, column=0, sticky='NE')
        Button(self, text="New ADs(<10)", command=self.newads).grid(row=2, column=1, sticky='NE')
        Button(self, text="Old ADs(>20)", command=self.oldads).grid(row=3, column=1, sticky='NE')
        Label(self,text='room count , age , area , user :').grid(row=5, column=1, sticky='SW')


        file = open('ads.csv')
        reader = csv.reader(file)
        reader = list(reader)
        file.close()
        ad_number = len(reader)
        for i in range(ad_number):
            Label(self, text=str(reader[i])).grid(row=i + 7, column=1, sticky='SW')

    def oldads(self):
        self.controller.show_frame("OldAdsFrame")
    def newads(self):
        self.controller.show_frame("NewAdsFrame")

    def ad(self):
        self.controller.show_frame("AdFrame")

    def logout(self):
        self.controller.user = User(-1)
        self.controller.show_frame("LoginFrame")

    def refresh(self):
        self.toolbar_frame = Frame(self).grid(row=4, columnspan=2, sticky='NSEW')
        toolbar_frame = Frame(self)
        toolbar_frame.grid(row=4, columnspan=2, sticky=S + E + W)
        self.welcome_msg.set("Hello %s!" % self.controller.user.username)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)


class NewAdsFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.welcome_msg = StringVar(parent)
        Label(self, textvariable=self.welcome_msg).grid(row=1, column=0, sticky='NW')
        Button(self, text="Return", command=self.close).grid(row=1, column=1, sticky='NE')

        self.content = StringVar()
        file = open('ads.csv')
        reader = csv.reader(file)
        reader = list(reader)
        file.close()
        ad_number = len(reader)
        new_properies = []
        for i in range(ad_number):
            if int(reader[i][1]) < 10:
                new_properies.append(i)
        for i in range(len(new_properies)):
            Label(self, text=str(reader[new_properies[i]])).grid(row=i + 2, column=0, sticky='SW')

    def close(self):
        self.controller.show_frame("UserFrame")


class OldAdsFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.welcome_msg = StringVar(parent)
        Label(self, textvariable=self.welcome_msg).grid(row=1, column=0, sticky='NW')
        Button(self, text="Return", command=self.close).grid(row=1, column=1, sticky='NE')

        self.content = StringVar()
        file = open('ads.csv')
        reader = csv.reader(file)
        reader = list(reader)
        file.close()
        ad_number = len(reader)
        old_properties = []
        for i in range(ad_number):
            if int(reader[i][1]) > 20:
                old_properties.append(i)
        for i in range(len(old_properties)):
            Label(self, text=str(reader[old_properties[i]])).grid(row=i + 2, column=0, sticky='SW')

    def close(self):
        self.controller.show_frame("UserFrame")


class RegisterFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller

        self.usEntry_reg = StringVar(parent)
        Label(self, text="Username").grid(row=0, column=0)
        Entry(self, textvariable=self.usEntry_reg).grid(row=0, column=1)

        self.pass1 = StringVar(parent)
        self.pass1.set('')
        self.pass2 = StringVar(parent)
        self.pass2.set('')

        Label(self, text="Password").grid(row=1, column=0)
        Entry(self, show="*", textvariable=self.pass1).grid(row=1, column=1)

        Label(self, text="re-enter Password").grid(row=2, column=0)
        Entry(self, show="*", textvariable=self.pass2).grid(row=2, column=1)

        Button(self, borderwidth=4, text="Register", width=10, pady=4, command=self.create_account).grid(row=3,
                                                                                                         column=1)
        Button(self, borderwidth=4, text="Return", width=10, pady=4,
               command=lambda: self.controller.show_frame("LoginFrame")).grid(row=4, column=1)

    def refresh(self):
        self.pass1.set('')
        self.pass2.set('')
        self.usEntry_reg.set('')

    def create_account(self):
        if self.pass1.get() != self.pass2.get():
            self.pass1.set('')
            self.pass2.set('')
            messagebox.showwarning("Password not match.", "Please verify your password again.")
        elif self.pass1.get() == '':
            messagebox.showwarning("Blank fields.", "Please do not leave any fields blank.")
        else:
            try:
                db.register(self.usEntry_reg.get(), self.pass1.get())
                messagebox.showinfo("Account created.", "Please login using new credentials. :)")
            except:
                messagebox.showwarning("Error.", "Please try another username or contact a technician")
            self.controller.show_frame("LoginFrame")
            self.controller.frames['LoginFrame'].usEntry.set(self.usEntry_reg.get())


class LoginFrame(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.grid(row=0, column=0)
        self.usEntry = StringVar()
        self.pwEntry = StringVar()

        Label(self, text="Username").grid(row=0, column=0)
        Entry(self, textvariable=self.usEntry).grid(row=0, column=1)

        Label(self, text="Password").grid(row=1, column=0)
        Entry(self, show="*", textvariable=self.pwEntry).grid(row=1, column=1)

        self.btn_login = Button(self, borderwidth=4, text="Login", width=10, pady=4, command=self.check_password)
        self.btn_login.grid(row=2, column=1, columnspan=2)
        self.lbl_status = StringVar(parent)
        self.lbl_status.set("waiting input...")
        Button(self, borderwidth=4, text="Register", width=10, pady=4,
               command=lambda: self.controller.show_frame("RegisterFrame")).grid(row=3, column=1, columnspan=2)

        Label(self, textvariable=self.lbl_status).grid(row=4, column=0, columnspan=2, sticky='W')

    def refresh(self):
        self.pwEntry.set('')
        self.lbl_status.set("IDLE.")
        self.usEntry.set('')

    def check_password(self):
        self.user_id = db.getuserid(self.usEntry.get(), self.pwEntry.get())
        self.pwEntry.set('')
        if self.user_id == -1:
            self.login_failure()
        else:
            self.usEntry.set('')
            self.login_success()

    def login_success(self):
        self.lbl_status.set("Login succeed.")
        self.controller.user = User(self.user_id)
        self.controller.show_frame("UserFrame")

    def login_failure(self):
        self.lbl_status.set("Authentication failed.")


class AdFrame(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)
        self.controller = controller
        self.room_count = StringVar()
        self.age = StringVar()
        self.area = StringVar()
        Label(self, text="room count").grid(row=0, column=0)
        Entry(self, textvariable=self.room_count).grid(row=0, column=1)

        Label(self, text="age").grid(row=1, column=0)
        Entry(self, textvariable=self.age).grid(row=1, column=1)

        Label(self, text="area").grid(row=2, column=0)
        Entry(self, textvariable=self.area).grid(row=2, column=1)

        Button(self, borderwidth=4, text="Add", width=10, pady=4, command=self.new_ad).grid(row=3, column=1)
        Button(self, borderwidth=4, text="Return", width=10, pady=4,
               command=lambda: self.controller.show_frame("UserFrame")).grid(row=4, column=1)

    def new_ad(self):
        try:
            db.newad(self.room_count.get(), self.age.get(), self.area.get(), self.controller.user.username)
            messagebox.showinfo("ad created.", "succussfully created ;) ")
        except:
            messagebox.showwarning("Error.", "something is wrong . please try again!")
        self.controller.show_frame("UserFrame")


class SampleApp(Tk):

    def onFrameConfigure(self, canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))

    def FrameWidth(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_frame, width=canvas_width)

    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.canvas = Canvas(self, borderwidth=0, background="#ffffff")
        self.user = User(-1)
        container = Frame(self.canvas)
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_frame = self.canvas.create_window((4, 4), window=container, anchor="nw")

        container.bind("<Configure>", lambda event, canvas=self.canvas: self.onFrameConfigure(canvas))
        self.canvas.bind('<Configure>', self.FrameWidth)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (LoginFrame, RegisterFrame, UserFrame, AdFrame, NewAdsFrame, OldAdsFrame):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginFrame")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        try:
            frame.refresh()
        except AttributeError:
            pass

        frame.tkraise()


class Login(Tk):
    def register(self):
        pass


def main():
    app = SampleApp()
    app.mainloop()


if __name__ == '__main__': main()
