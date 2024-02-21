#!/usr/bin/env python3
import customtkinter,tkinter
from tkinter import*
import rospy
from std_msgs.msg import Int16
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")
frame = customtkinter.CTk()
frame.title("GUI REMOTE")
frame.geometry("1000x600")
rospy.init_node("GUI_new1_1", anonymous=True)

pubtojoint = rospy.Publisher('joint_states', JointState, queue_size=10)
read1 = 0
read2 = 0

def setup():
    msg = JointState()
    msg.name = ['joint1', 'joint2'];  
    msg.position = [0,0]
    pubtojoint.publish(msg)

rate = rospy.Rate(10)
rate.sleep()
system_state = "ON"
frame.after(1000,setup)

def readS1(num):
    global system_state
    global encoder_read
    encoder_read = num.data 
    if system_state == "ON":
        L1.config(text = str(encoder_read))
 

def readS2(num2):
    global system_state
    global poten_read
    poten_read = num2.data
    if system_state == "ON":
        L2.config(text=str(poten_read))


def send_data():
    global poten_read
    global encoder_read
    global system_state
    if system_state == "ON":
        msg = JointState()
        rate = rospy.Rate(10) # 10hz
        print(encoder_read)
        print(poten_read)
        msg.name = ['joint1', 'joint2']
        msg.position = [encoder_read*0.002481,poten_read*(0.272*10**-3)] 
        msg.header.stamp = rospy.Time.now()
        pubpoten.publish(poten_read)
        pubencoder.publish(encoder_read)
        pubtojoint.publish(msg)

def send_slider():
    global read1
    global read2
    global system_state
    if system_state == "ON":
        msg = JointState()
        rate = rospy.Rate(10) # 10hz
        msg.name = ['joint1', 'joint2']
        msg.position = [read1*0.002481,read2*(0.272*10**-3)] 
        msg.header.stamp = rospy.Time.now()
        pubpoten.publish(read2)
        pubencoder.publish(read1)
        pubtojoint.publish(msg)
    
pubpoten = rospy.Publisher("Poten_Run", Float64, queue_size=10)
pubencoder = rospy.Publisher("Encoder_Run", Float64, queue_size=10)

frame = customtkinter.CTkFrame(master = frame,fg_color= "#BEBEBE")
frame.pack(padx = 1,pady = 1,fill="both",expand=True)

def slider_event(value):
    global read1
    global read2
    global system_state
    if system_state == "ON":
        read1 = int(slider.get())
        read2 = int(slider2.get())
        L3.config(text= str(read1))## รับข้อความ
        L4.config(text= str(read2))## รับข้อความ

sub1= rospy.Subscriber("poten_angle", Float64,callback=readS2)
sub= rospy.Subscriber("servo_angle", Int16,callback=readS1)

slider = customtkinter.CTkSlider(master=frame,from_=0,to=180,command=slider_event)
slider.place(x=320,y=510,anchor=tkinter.W)


def button_on():
    global system_state
    print("ON")
    system_state = "ON"

def button_off():
    global system_state
    print("OFF")
    system_state = "OFF"



L1 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L1.place(x=380, y=200)

L2 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L2.place(x=730, y=200)

L3 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L3.place(x=380, y=380)

L4 = Label(frame,font = ('Arial',60),text ="00",bg="#BEBEBE")
L4.place(x=730, y=380)


namepro = tkinter.StringVar(value="RP ROBOT")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=namepro,
                               width=120,
                               height=25,
                               font=('Hello',30),
                               text_color="black",
                               fg_color=("white", "gray75"),
                               corner_radius=8)
label.place(x=55, y=55, anchor=tkinter.W)


frame1 = customtkinter.CTkFrame(frame,fg_color= "#DCDCDC", width=250,height=500, corner_radius=10)
frame1.grid(row=0, column=0, padx=0, pady=100, sticky="ew")

text_var = tkinter.StringVar(value=" MODE ")
label = customtkinter.CTkLabel(master=frame1,
                               textvariable=text_var,
                               width=225,
                               height=50,
                               fg_color=("#424242"),
                               text_color="white",
                               corner_radius=8)
label.place(x=13, y=40, anchor=tkinter.W)

button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="green", 
                                 hover_color="grey",
                                 border_width=0,
                                 corner_radius=8,
                                 text="ON",
                                 command=button_on)
button.place(x=10, y=400, anchor=tkinter.W)



button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="red", 
                                 hover_color="gray",
                                 border_width=0,
                                 corner_radius=8,
                                 text="OFF",
                                 command=button_off)
button.place(x=150, y=400, anchor=tkinter.W)

button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="#ffc107", 
                                 text_color="black",
                                 hover_color="gray",
                                 border_width=0,
                                 corner_radius=8,
                                 text="SENT DATA",
                                 command=send_data)
button.place(x=30, y=100, anchor=tkinter.W)

nameJ1 = tkinter.StringVar(value=" JOINT 1 ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameJ1,
                               width=160,
                               height=50,
                               font=('Arial',15),
                               text_color="white",
                               fg_color=("#000000"),
                               corner_radius=30)
label.place(x=350, y=70, anchor=tkinter.W)

nameEn = tkinter.StringVar(value=" ENCODER ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameEn,
                               font=('Arial',20),
                               text_color="black",)
label.place(x=380, y=120, anchor=tkinter.W)

realvale_encoder = tkinter.StringVar(value="Manual Mode")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=350,y=160,anchor=tkinter.W)


usevale_encoder = tkinter.StringVar(value="GUI MODE")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=350,y=340,anchor=tkinter.W)

nameJ2 = tkinter.StringVar(value=" JOINT 2 ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=nameJ2,
                               width=160,
                               height=50,
                               font=('Arial',15),
                               text_color="white",
                               fg_color=("#000000"),
                               corner_radius=30)
label.place(x=700, y=70, anchor=tkinter.W)

namePo = tkinter.StringVar(value=" POTENTIOMETER ")
label = customtkinter.CTkLabel(master=frame,
                               textvariable=namePo,
                               font=('Arial',20),
                               text_color="black",)
label.place(x=690, y=120, anchor=tkinter.W)

realvale_encoder = tkinter.StringVar(value="Manual Mode")
labelr = customtkinter.CTkLabel(master = frame,textvariable = realvale_encoder ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=700,y=160,anchor=tkinter.W)
    

usevale_poten = tkinter.StringVar(value="GUI Mode")
labelr = customtkinter.CTkLabel(master = frame,textvariable = usevale_poten ,width=150,height=30,
                                fg_color=("#757575"),
                                text_color="white",
                                font=('Arial',15),
                                corner_radius=8)
labelr.place(x=700,y=340,anchor=tkinter.W)

slider2 = customtkinter.CTkSlider(master=frame,from_=0,to=180,command=slider_event)
slider2.place(x=680,y=510,anchor=tkinter.W)

button = customtkinter.CTkButton(master=frame1,
                                 width=80,
                                 height=32,
                                 fg_color="#01579b", 
                                 text_color="white",
                                 hover_color="gray",
                                 border_width=0,
                                 corner_radius=8,
                                 text="SENT SLIDER",
                                 command=send_slider)
button.place(x=130, y=100, anchor=tkinter.W)





frame.mainloop()