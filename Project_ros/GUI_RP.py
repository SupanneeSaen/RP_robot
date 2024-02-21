#!/usr/bin/env python3
import customtkinter,tkinter
from tkinter import*
import rospy
from std_msgs.msg import Int16
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

# frame = Tk()
frame = customtkinter.CTk()
# fram1 = customtkinter.CTkFrame(master=app,width=400,height=400,corner_radius=10)
# fram1.pack(padx=20,pady=20)
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
frame.title("REMOTE")
frame.geometry("550x550")
rospy.init_node("GUI_RP")
pub = rospy.Publisher("servo_angle",Twist, queue_size=10)
rate = rospy.Rate(10)
rate.sleep()


# Canvas1 = Canvas(frame, width=285, height=550, bg='white')
# Canvas1.grid(row=0, column=0, padx=10, pady=2)

# Canvas2 = Canvas(frame, width=275, height=550, bg='white')
# Canvas2.place(x=275, y=0)

L1 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
#L.pack()
L1.place(x=105, y=160)

L2 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
#L.pack()
L2.place(x=360, y=160)

L3 = Label(frame,font = ('Arial',60),text ="00")
#L.pack()
L3.place(x=105, y=300)

L4 = Label(frame,font = ('Arial',60),text ="00")
#L.pack()
L4.place(x=360, y=300)

Name = Label(frame,font = ('Arial',10), text=" RP PROJECT ",bg="#4F80C0")
# first.grid(row=150, column=0, padx=10, pady=2)
Name.place(x=210, y=5)

Joint1 = Label(frame,font = ('Arial',10), text=" JOINT 1 ",bg="#4F80C0")
# first.grid(row=150, column=0, padx=10, pady=2)
Joint1.place(x=120, y=40)

Joint2 = Label(frame,font = ('Arial',10), text=" JOINT 2 ",bg="#4F80C0")
# first.grid(row=150, column=0, padx=10, pady=2)
Joint2.place(x=380, y=40)

encodername = Label(frame,font = ('Arial',10), text=" ENCODER ",bg="#4F80C0")
# first.grid(row=150, column=0, padx=10, pady=2)
encodername.place(x=110, y=70)

potenname = Label(frame,font = ('Arial',10), text=" POTENTIOMETER ",bg="#4F80C0")
# first.grid(row=150, column=0, padx=10, pady=2)
potenname.place(x=350, y=70)

realvale_encoder = tkinter.StringVar(value="Real Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_encoder ,width=120,height=25,
                                fg_color=("black","black"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(relx=0.1,rely=0.25,anchor=tkinter.W)

realvale_poten = tkinter.StringVar(value="Real Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_poten ,width=120,height=25,
                                fg_color=("black","black"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(relx=0.58,rely=0.25,anchor=tkinter.W)

usevale_encoder = tkinter.StringVar(value="USE Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_encoder ,width=120,height=25,
                                fg_color=("black","black"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(relx=0.1,rely=0.5,anchor=tkinter.W)

usevale_poten = tkinter.StringVar(value="USE Value")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_poten ,width=120,height=25,
                                fg_color=("black","black"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(relx=0.58,rely=0.5,anchor=tkinter.W)


def slider_event(value):
    text_var.set(f"{int(slider.get())}")
    text_var2.set(f"{int(slider2.get())}")
    # V1 = text_var
    # V2 = text_var2
    print("encoder value = "+str(text_var.get()))
    print("poten value = "+str(text_var2.get()))
    
    # print(V2)
 

# def slider_event2(value):
#     text_var.set(f"{int(slider2.get())}")

def readS1(num):
    servo_read = num.data 
    L1.config(text = str(servo_read))## รับข้อความ
    print(servo_read)
sub= rospy.Subscriber("servo_angle", Int16,callback=readS1)


def readS2(num1):
    poten_read = num1.data 
    L2.config(text = str(poten_read))## รับข้อความ
    print(poten_read)
sub= rospy.Subscriber("poten_angle", Int16,callback=readS2)


def ON():
    print("ON")

def OFF():
    print("OFF")

def Degree():
    print("degree")




slider = customtkinter.CTkSlider(master=frame,from_=0,to=90,command=slider_event)
slider.place(relx=0.1,rely=0.78,anchor=tkinter.W)

text_var = tkinter.StringVar(value="0")
labelr = customtkinter.CTkLabel(master = frame,textvariable = text_var,width=120,height=25,
                                fg_color=("green","black"),
                                text_color="white",
                                font=('Arial',20),
                                corner_radius=8)
labelr.place(relx=0.17,rely=0.85,anchor=tkinter.W)

slider2 = customtkinter.CTkSlider(master=frame,from_=0,to=90,command=slider_event)
slider2.place(relx=0.55,rely=0.78,anchor=tkinter.W)

text_var2 = tkinter.StringVar(value="0")
labelr2 = customtkinter.CTkLabel(master = frame, textvariable = text_var2 ,width=120,height=25,
                                fg_color=("green","black"),
                                text_color="white",
                                font=('Arial',20),
                                corner_radius=8)
labelr2.place(relx=0.62,rely=0.85,anchor=tkinter.W)

B1 = Button(text = "ON", command=ON,bg="#4F80C0")
B1.place(x=140, y=500)

B2 = Button(text = "OFF", command=OFF,bg="#4F80C0")
B2.place(x=330, y=500)


frame.mainloop()