import pygame
from pygame.locals import *
import random
from tkinter import *
import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk
import PIL
import smtplib
from pymongo import MongoClient
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

window = Tk()
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()


pygame.mixer.music.load('music/loginbackground.mp3')
pygame.mixer.music.play(-1)

def resize_image(event):
    new_width = event.width
    new_height = event.height
    image = copy_of_image.resize((new_width, new_height))
    photo = ImageTk.PhotoImage(image)
    label.config(image = photo)
    label.image = photo #avoid garbage collection

def send_coad(receiver_address,mail_content):
    sender_address = 'fruit.basket.team.14@gmail.com'
    sender_pass = 'FruitBasket'
    #receiver_address = 'jayeshagrawal07@gmail.com'
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'Fruit Basket Email Verification Code '   #The subject line
    message.attach(MIMEText(mail_content, 'plain'))
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()




global login_variable


cluster=MongoClient("mongodb+srv://FruitBasketdb:FruitBasketdb@fruitbasketcluster.x9fnm.mongodb.net/FruitBasketdb?retryWrites=true&w=majority")

db=cluster["FruitBasketdb"]
collection=db["FruitBasket_User"]




window.title("Welcome to Fruit Basket Login Form")
window.attributes('-fullscreen', True)
def Check_forget_otp():
    if New_Pswrd.get()=="" and New_CPswrd.get()=="":
        messagebox.showwarning("Warning", "Password Fields is Required !!")
    elif New_Pswrd.get()!=New_CPswrd.get():
        messagebox.showwarning("Warning", "OTP Did not Match !")
    elif Otp_entry.get()==str(coad_forget):
        collection.update_one({"_id": Forget_mail.get()}, {"$set": {"User_Pswrd_Register":New_Pswrd.get()}})
        main_page()
    else:
        messagebox.showwarning("Warning", "OTP Did not Match !")

def Check_email():
    if Forget_mail.get()=="":
        messagebox.showwarning("Warning", "Email Field is Required !")
    elif collection.count_documents({"_id": Forget_mail.get()}) > 0:
        global coad_forget,Otp_entry,New_Pswrd,New_CPswrd
        coad_forget = random.randint(100000, 999999)
        mail_content_reset = '''Hi,

        Your verification code for reset the Password of Fruit Basket Game is :    ''' + str(coad_forget) + '''	 

        If you did not request this, Please ignore.	 

        Thanks,
        Vishwas Katiyar
        Fruit Basket Game 
        '''

        send_coad(Forget_mail.get(),mail_content_reset)
        messagebox.showwarning("Warning", "Email for reset password is Sent to " + Forget_mail.get() + " Please check")


        NewPasswordFrame = Frame(highlightbackground="brown", highlightcolor="red", highlightthickness=5, width=100,
                                   height=100, bg="white")
        NewPasswordFrame.place(x=(window.winfo_screenwidth()//2)-250,y=(window.winfo_screenheight()//2)-200,height=400,width=500)

        a = Label(NewPasswordFrame, text="   NEW PASSWORD", font=(font1, 30, "bold"), fg="brown", bg="white")
        a.place(x=50, y=25)

        a = Label(NewPasswordFrame, text="NEW PASSWORD", font=(font1, 15, "bold"), fg="brown", bg="white")
        a.place(x=20, y=150)
        New_Pswrd = Entry(NewPasswordFrame,font=(font1,15), show='*', bg="#F48B5D")
        New_Pswrd.place(x=250, y=150, width=200, height=30)

        a = Label(NewPasswordFrame, text="CONFIRM PASSWORD", font=(font1, 15, "bold"), fg="brown", bg="white")
        a.place(x=20, y=210)
        New_CPswrd = Entry(NewPasswordFrame, show='*',font=(font1,15), bg="#F48B5D")
        New_CPswrd.place(x=250, y=210, width=200, height=30)

        a = Label(NewPasswordFrame, text="ENTER OTP", font=(font1, 15, "bold"), fg="brown", bg="white")
        a.place(x=20, y=270)
        Otp_entry = Entry(NewPasswordFrame,font=(font1,15), bg="#F48B5D")
        Otp_entry.place(x=250, y=270, width=200, height=30)

        check_Otp_button = tk.Button(NewPasswordFrame, command=Check_forget_otp, font=(font1, 15), text="SUBMIT", bg="#4CAF50",
                               fg="white")
        check_Otp_button.place(x=250, y=350, width=100, height=30)
        backtoforget_button = tk.Button(NewPasswordFrame, command=forget_btn, font=(font1, 15), text="BACK",
                                     bg="#4CAF50",
                                     fg="white")
        backtoforget_button.place(x=120, y=350, width=100, height=30)

    else :
        messagebox.showwarning("Warning", "Email Not Registered ! Please Register Now !!")


def forget_btn():
    Forget_Frame = Frame(highlightbackground="brown", highlightcolor="red", highlightthickness=5, width=100,height=100, bg="white")
    Forget_Frame.place(x=(window.winfo_screenwidth()//2)-250,y=(window.winfo_screenheight()//2)-200,height=400,width=500)

    a = Label(Forget_Frame, text="FORGET PASSWORD", font=(font1, 30, "bold"), fg="brown", bg="white")
    a.place(x=50, y=25)
    a = Label(Forget_Frame, text="( Please Enter the Email linked with FruitBasket )", font=(font1, 15, "bold"), fg="brown", bg="white")
    a.place(x=40, y=100)

    a = Label(Forget_Frame, text=" USER EMAIL ID : ", font=(font1, 20, "bold"), fg="brown", bg="white")
    a.place(x=20, y=195)
    global Forget_mail
    Forget_mail = Entry(Forget_Frame,font=(font1,15), bg="#F48B5D")
    Forget_mail.place(x=250, y=200, width=200, height=30)

    #forget_Otp_entry = Entry(Forget_Frame, bg="#F48B5D")
    #forget_Otp_entry.place(x=250, y=220, width=200, height=30)
    Otp_button = tk.Button(Forget_Frame, command=Check_email, font=(font1, 15), text="SUBMIT", bg="#4CAF50",fg="white")
    Otp_button.place(x=250, y=350, width=100, height=30)
    back_btn = tk.Button(Forget_Frame, command=main_page, font=(font1, 15), text="BACK", bg="#4CAF50", fg="white")
    back_btn.place(x=120, y=350, width=100, height=30)

    # global coad1,Otp_entry


def Check_otp():
    if str(coad1) == Otp_entry.get():
        collection.insert_one({"_id":User_Email.get(),"User_Name_Register":User_Name_Register.get(),"User_Pswrd_Register":User_Pswrd_Register.get(),"User_Email":User_Email.get(),"score" : 0})
        main_page()
    else:
        messagebox.showwarning("Warning","Otp Is Not Correct !")
     
def Register_me():
    regexmail = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    regexno='fg'
        
    if User_Name_Register.get()!="" and User_Pswrd_Register.get()!="" and User_Email.get()!="":
        if User_Pswrd_Register.get()!=User_CPswrd_Register.get():
            messagebox.showwarning("Warning","Create Password and Confirm Password Must be same !")
        elif collection.count_documents({"_id":User_Email.get()}) > 0:
            messagebox.showwarning("Warning","Email is Already in Use !")
     
        elif User_Email.get()!="":
            global coad1,Otp_entry
            coad1 = random.randint(100000, 999999)
            mail_content = '''Hi, ''' + User_Name_Register.get() + '''

            Your verification code for Fruit Basket Game is: ''' + str(coad1) + '''	 

            If you did not request this, Please ignore.	 

            Thanks,
            Vishwas Katiyar
            Fruit Basket Game

            '''
            Verification_Frame=Frame( highlightbackground="brown", highlightcolor="red", highlightthickness=5, width=100, height=100, bg="white")
            Verification_Frame.place(x=(window.winfo_screenwidth()//2)-250,y=(window.winfo_screenheight()//2)-200,height=400,width=500)

            a = Label(Verification_Frame ,text = "Verify OTP",font=(font1,30,"bold"),fg="brown",bg="white")
            a.place(x=170,y=25)
            a = Label(Verification_Frame ,text = "OTP",font=(font1,20,"bold"),fg="brown",bg="white")
            a.place(x=20,y=220)
            Otp_entry = Entry(Verification_Frame,font=(font1,15),bg="#F48B5D")
            Otp_entry.place(x=250,y=220,width=200,height=30)
            Otp_button = tk.Button(Verification_Frame,command=Check_otp,font=(font1,15) ,text="SUBMIT",bg="#4CAF50",fg="white")
            Otp_button.place(x=150,y=350,width=200,height=30)
            #global coad1,Otp_entry
            send_coad(User_Email.get(),mail_content)
            messagebox.showwarning("Warning","Email is Sent to "+User_Email.get()+" Please check")
        
    
    else:
        #a = Label(window ,text = "All Fields Are Required ",font=(font1,30,"bold"),fg="white")
        messagebox.showwarning("Warning","All Fields Are Required !")
     

def Quit_btn():
    login_variable=False
    pygame.quit()
    window.destroy()
def login_btn():
    #print(User_Name.get())
    #print(User_Pswrd.get())
    global loggedin_email
    if User_login_email.get()==""  or User_login_Pswrd.get()=="":
        
        #print("All Fields are Required !")
        #a = Label(Frame_Register ,text = "REGISTER",font=(font1,30,"bold"),fg="brown",bg="white").place(x=170,y=25)
        messagebox.showwarning("warning","All Fields are Required !")
    else:
        if collection.count_documents({"_id":User_login_email.get()}) > 0:
            details=collection.find({"_id":User_login_email.get()})
            #print(details)
            for detail in details :
                #print(detail)
                if detail["_id"]==User_login_email.get() and detail["User_Pswrd_Register"]==User_login_Pswrd.get():
                    global login_variable,loginned_name
                    loginned_name=detail["User_Name_Register"]
                    #server_score=detail["score"]
                    login_variable=True
                    loggedin_email=User_login_email.get()
                    window.destroy()
                else:
                    messagebox.showwarning("warning","Incorect Password!")
        else:
            messagebox.showwarning("Warning","Please provide User Name & Password ")
        
def Register_btn():
    #print("Register Page")
    Frame_Register=Frame( highlightbackground="brown", highlightcolor="red", highlightthickness=5, width=100, height=100, bg="white")
    Frame_Register.place(x=(window.winfo_screenwidth()//2)-250,y=(window.winfo_screenheight()//2)-200,height=400,width=500)

    a = Label(Frame_Register ,text = "REGISTER ",font=(font1,30,"bold"),fg="brown",bg="white")
    a.place(x=170,y=25)
    a = Label(Frame_Register ,text = "USER NAME ",font=(font1,15,"bold"),fg="brown",bg="white")
    a.place(x=20,y=100)
    b = Label(Frame_Register ,text = "CREATE PASSWORD  ",font=(font1,15,"bold"),fg="brown",bg="white")
    b.place(x=20,y=170)
    b = Label(Frame_Register ,text = "CONFIRM PASSWORD  ",font=(font1,15,"bold"),fg="brown",bg="white")
    b.place(x=20,y=240)
    c = Label(Frame_Register ,text = "EMAIL ID ",font=(font1,15,"bold"),fg="brown",bg="white")
    c.place(x=20,y=310)
    
    global User_Name_Register,User_Pswrd_Register,User_Email,User_CPswrd_Register
    User_Name_Register = Entry(Frame_Register,font=(font1,15),bg="#F48B5D")
    User_Name_Register.place(x=250,y=100,width=200,height=30)
    User_Pswrd_Register = Entry(Frame_Register,font=(font1,15), show= '*',bg="#F48B5D")
    User_Pswrd_Register.place(x=250,y=160,width=200,height=30)
    User_CPswrd_Register = Entry(Frame_Register,font=(font1,15), show= '*',bg="#F48B5D")
    User_CPswrd_Register.place(x=250,y=230,width=200,height=30)
    User_Email = Entry(Frame_Register,font=(font1,15),bg="#F48B5D")
    User_Email.place(x=250,y=300,width=200,height=30)
    
    #Email_Id = Entry(window).grid(row = 2,column = 1)
    #Contact_Number = Entry(window).grid(row = 3,column = 1)

    #Register_Button = tk.Button(Frame_Register,command=Register_me,font=(font1,15) ,text="REGISTER",bg="#4CAF50",fg="white")
    #Register_Button.place(x=150,y=350,width=200,height=30)
    Register_Button = tk.Button(Frame_Register,command=Register_me,font=(font1,15) ,text="SUBMIT",bg="#4CAF50",fg="white")
    Register_Button.place(x=250,y=350,width=100,height=30)
    btn_Back = tk.Button(Frame_Register,command=main_page,font=(font1,15) ,text="BACK",bg="#4CAF50",fg="white")
    btn_Back.place(x=120,y=350,width=100,height=30)
    

image = Image.open('images/background.jpg')
copy_of_image = image.copy()
photo = ImageTk.PhotoImage(image)
label = tk.Label(window, image = photo)
label.bind('<Configure>', resize_image)
label.pack(fill=BOTH, expand = YES)
font1="Goudy Old Style"

#c = Label(window ,text = "Email Id").grid(row = 2,column = 0)
#d = Label(window ,text = "Contact Number").grid(row = 3,column = 0)
def main_page():
    Frame_login=Frame( highlightbackground="brown", highlightcolor="red", highlightthickness=5, width=100, height=100, bg="white")
    Frame_login.place(x=(window.winfo_screenwidth()//2)-250,y=(window.winfo_screenheight()//2)-200,height=400,width=500)
    
    #img = PhotoImage(file='images/loginicon.png')
    #.resize(20, 20) # the one-liner I used in my app
    #label = Label(Frame_login, image=img).place(x=20,y=20,height=200,width=200)
    #fp = open('images/loginicon.png',"rb")
    #img = PIL.Image.open(fp)
    #img.show()
    load = PIL.Image.open('images/loginicon.png')
    render = ImageTk.PhotoImage(load)
    img = Label(Frame_login,image=render)
    img.image = render
    img.place(x=50, y=50,width=110,height=110)

    a = Label(Frame_login ,text = "  LOGIN",font=(font1,30,"bold"),fg="brown",bg="white").place(x=200,y=70)
    a = Label(Frame_login ,text = "USER EMAIL:",font=(font1,15,"bold"),fg="brown",bg="white").place(x=35,y=200)
    b = Label(Frame_login ,text = "PASSWORD  :",font=(font1,15,"bold"),fg="brown",bg="white").place(x=35,y=250)

    global User_login_email ,User_login_Pswrd,loggedin_email
    User_login_email = Entry(Frame_login,font=(font1,15),bg="#F48B5D")
    User_login_email.place(x=250,y=200,width=200,height=30)
    User_login_Pswrd = Entry(Frame_login, show= '*',font=(font1,15),bg="#F48B5D")
    User_login_Pswrd.place(x=250,y=250,width=200,height=30)
    #Email_Id = Entry(window).grid(row = 2,column = 1)
    #Contact_Number = Entry(window).grid(row = 3,column = 1)

    btn_Submit = tk.Button(Frame_login,command=login_btn,font=(font1,15) ,text="SUBMIT",bg="#4CAF50",fg="white").place(x=250,y=350,width=100,height=30)
    btn_Quit = tk.Button(Frame_login,command=Quit_btn,font=(font1,15) ,text="QUIT",bg="#4CAF50",fg="white").place(x=120,y=350,width=100,height=30)
    btn_Register = tk.Button(Frame_login,command=Register_btn,font=(font1,15) ,bd=0,text="REGISTER HERE !",bg="white",fg="brown").place(x=20,y=300,width=200,height=30)
    btn_Forget = tk.Button(Frame_login, command=forget_btn, font=(font1, 15), bd=0, text="FORGET PASSWORD ?",bg="white", fg="brown").place(x=250, y=300, width=200, height=30)


main_page()
window.mainloop()


score = 0
lives = 3

#textinput = pygame_textinput.TextInput()
#backgroundimg1 = pygame.image.load("background1.jpg")

screen = pygame.display.set_mode((1366,768 ),FULLSCREEN)
#print('Height :   : ',screen.get_height())
#print('Width :   : ',screen.get_width())
#screen = pygame.display.set_mode((800,)
pygame.display.set_caption("apple")


x=650
y=screen.get_height()-105


backgroundimg = pygame.image.load("images/background.jpg").convert_alpha()
backgroundimg = pygame.transform.scale(backgroundimg,(screen.get_width(),screen.get_height()))
#backgroundimg_rect=backgroundimg.get_rect()


basket = pygame.image.load("images/basket.png").convert_alpha()
basket = pygame.transform.scale(basket, ( basket.get_width() //3 ,basket.get_height() //3))
#print("@@@@@@@@@@@@@@@@@@@@@",basket.get_width() //3)

apple=pygame.image.load("images/apple.png").convert_alpha()
apple=pygame.transform.scale(apple, ( apple.get_width() //2 ,apple.get_height() //2))

egg=pygame.image.load("images/egg.png").convert_alpha()
egg=pygame.transform.scale(egg, ( egg.get_width() //40 ,egg.get_height() //40))


bomb=pygame.image.load("images/bomb.png").convert_alpha()
bomb=pygame.transform.scale(bomb, ( bomb.get_width() //10 ,bomb.get_height() //10))

mango=pygame.image.load("images/mango.png").convert_alpha()
mango=pygame.transform.scale(mango, ( mango.get_width() //10 ,mango.get_height() //10))


grapes=pygame.image.load("images/grapes.png").convert_alpha()
grapes=pygame.transform.scale(grapes, ( grapes.get_width() //10 ,grapes.get_height() //10))

guava=pygame.image.load("images/guava.png").convert_alpha()
guava=pygame.transform.scale(guava, ( guava.get_width() //10 ,guava.get_height() //10))

star=pygame.image.load("images/star.png").convert_alpha()
star=pygame.transform.scale(star, ( star.get_width() //10 ,star.get_height() //10))

watermelon=pygame.image.load("images/watermelon.png").convert_alpha()
watermelon=pygame.transform.scale(watermelon, ( watermelon.get_width() //12 ,watermelon.get_height() //12))

strawberry=pygame.image.load("images/strawberry.png").convert_alpha()
strawberry=pygame.transform.scale(strawberry, ( strawberry.get_width() //7 ,strawberry.get_height() //7))

coronavirus=pygame.image.load("images/coronavirus.png").convert_alpha()
coronavirus=pygame.transform.scale(coronavirus, ( coronavirus.get_width() //7 ,coronavirus.get_height() //7))


font = pygame.font.Font('fonts/font.otf', 56)


pygame.mixer.music.load('music/backgroundmusic.mp3')
pygame.mixer.music.play(-1)

#bg_sound = pygame.mixer.Sound("music/backgroundmusic.mp3")

#pygame.mixer.music.stop()

fall=pygame.mixer.Sound("music/falling.wav")
gameover=pygame.mixer.Sound("music/gameover.wav")
fallground=pygame.mixer.Sound("music/fallground.wav")
catch=pygame.mixer.Sound("music/catch.wav")
fallinbucket=pygame.mixer.Sound("music/fallinbucket.wav")
drop_ele=apple    

def drop_element(xofapple, yofapple):
    #drop_ele=random.choice([apple,egg])
    screen.blit(drop_ele,(round(xofapple), round(yofapple)))

def basketey(x, y):
    screen.blit(basket,(x, y))
add_drop_ele=star
def add_drop_element(xofapple, yofapple):
    #drop_ele=random.choice([apple,egg])
    screen.blit(add_drop_ele,(round(xofapple),round(yofapple)))


    '''ask(question) -> answer'''





ychange=0
xchange=0
yofadd_ele=20
up_score = 0
level=0
#add_drop_ele = random.choice([star,coronavirus,bomb])
xofadd_ele= random.randrange(10,screen.get_width()-66)
yofdrop_ele = 20
xofdrop_ele = random.randrange(10,screen.get_width()-66)
gameon=False
global leaderbaord
leaderbaord = False
def leaderboardfunction():
    leaderbaord = True

    while leaderbaord == True:
        y=(screen.get_height()//10)+100
        c=1
        screen.blit(backgroundimg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    leaderbaord = False
        start = "PLAYER "
        text = font.render(start, 1, (250, 250, 250))
        screen.blit(text, (screen.get_width()//5,screen.get_height()//10))

        start = "SCORE"
        text = font.render(start, 1, (250, 250, 250))
        screen.blit(text, (screen.get_width() //1.4, screen.get_height() // 10))

        start = "S.No."
        text = font.render(start, 1, (250, 250, 250))
        screen.blit(text, (screen.get_width() // 11, screen.get_height() // 10))

        # print("tototottototottoo"+str(topscoreonserver))
        for i in topscoreonserver:
            #" + i["User_Name_Register"] + "  Score ====" + str(i["score"]))

            sno = str(c)
            text = font.render(sno, 1, (250, 250, 250))
            screen.blit(text, (screen.get_width() // 10, y))

            uname = i["User_Name_Register"]
            text = font.render(uname, 1, (250, 250, 250))
            screen.blit(text, (screen.get_width()//5,y))

            scoreuser =  str(i["score"])
            text = font.render(scoreuser, 1, (250, 250, 250))
            screen.blit(text, (screen.get_width() // 1.4, y))
            y = y + 80
            c=c+1

            #pygame.display.update()

            back = "press B for Back"
            text = font.render(back, 1, (250, 250, 250))
            screen.blit(text, (screen.get_width() - 500, screen.get_height() - 100))

            pygame.display.update()

while login_variable==True:
    screen.blit(backgroundimg,(0,0))
    #print("We are here in while loop")    
    for event in pygame.event.get():
        #if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            #gameon = True
        if event.type == pygame.KEYDOWN:
            if event.key==pygame.K_s:
                gameon=True
                login_variable=False
            if event.key == pygame.K_l:
                topscoreonserver = collection.find(sort=[("score", -1)])
                leaderbaord=True
                leaderboardfunction()
    start = '''Welcome, '''+loginned_name
    text = font.render(start, 1, (250, 250, 250))
    screen.blit(text, (400,350))
    click = ''' Press S For Start Game !!!! '''
    text = font.render(click, 1, (250, 250, 250))
    screen.blit(text, (350, 450))
    click = ''' Press L For Leader-Board !!!! '''
    text = font.render(click, 1, (250, 250, 250))
    screen.blit(text, (350, 550))

    pygame.display.update()
speed=4
#gameon =





while True:
    while gameon == True:
    
        #screen.fill([255, 0, 0])
        screen.blit(backgroundimg,(0,0))
    #xofadd_ele = random.randrange(10,1300)
     
    
        if yofadd_ele < screen.get_height()-100 :
        #fallinbucket.play()
            yofadd_ele += speed - 0.8
            add_drop_element(xofadd_ele,yofadd_ele)
    
        if (screen.get_height()-90 > yofadd_ele > screen.get_height()-110) and (xofadd_ele in list(range(x-50,x+150)))  :
        #fallinbucket.play()
            if add_drop_ele == star:
                catch.play()
                lives=lives+1
                up_score = "Live +1"
            elif add_drop_ele == coronavirus:
                lives=lives-1
                score=score-30
                up_score ="-30  Live -1"
            elif add_drop_ele == bomb:
                score=score-10
                up_score="-10"
        

            add_drop_ele = random.choice([star,coronavirus,bomb])
        
            yofadd_ele=20
        
            xofadd_ele = random.randrange(10,screen.get_width())
            #yofadd_ele = yofadd_ele + ychange
        
            add_drop_element(xofadd_ele,yofadd_ele)
    
        elif yofadd_ele > screen.get_height()-110 :
            yofadd_ele=20
            xofadd_ele = random.randrange(10,screen.get_width())
            yofadd_ele = yofadd_ele + ychange
        
        #drop_element(xofdrop_ele, yofdrop_ele)
        
        #add_drop_element(xofadd_ele , yofadd_ele)
            add_drop_ele = random.choice([star,coronavirus,bomb])
            add_drop_element(xofadd_ele , yofadd_ele)
        
        add_drop_element(xofadd_ele , yofadd_ele)
        
#########################################################################################################3        
        if yofdrop_ele < screen.get_height()-100 :
            yofdrop_ele += speed
        #yofadd_ele += speed
        #drop_ele=random.choice([apple,egg])
            drop_element(xofdrop_ele, yofdrop_ele)
        
    #print(" fsdfs yofapple",yofapple)
    #print(" fsdfs x",x)
     
    
        
        if (screen.get_height()-90 > yofdrop_ele > screen.get_height()-110) and (xofdrop_ele in list(range(x-50,x+150)))  :
            fallinbucket.play()
        
            if level <= 4 :
                level=level+1
            elif level > 4 :
                level = int(str(speed)[0])
        
            if drop_ele in [egg,watermelon,grapes]:
                score = score + 10
                up_score = 10 
            elif drop_ele in [apple,strawberry] :
                score=score +15
                up_score = 15 
            elif drop_ele in [mango,guava]:
                score+=20
                up_score = 20 
        
        
    
        
            fall.play()
        
            drop_ele = random.choice([apple,egg,mango,guava,grapes,strawberry,watermelon])
            speed = speed+0.2
            #print("speedspeedspeed",speed)
            yofdrop_ele = 20
            xofdrop_ele = random.randrange(10,screen.get_width()-45)
        
            yofdrop_ele = yofdrop_ele+ychange
        #drop_ele=random.choice([apple,egg])
        #drop_element(xofdrop_ele, yofdrop_ele)
            drop_element(xofdrop_ele, yofdrop_ele)
    
        elif yofdrop_ele > screen.get_height()-110 : 
            fallground.play()
            yofdrop_ele=20
            xofdrop_ele = random.randrange(10,screen.get_width())
            yofdrop_ele=yofdrop_ele+ychange
            lives = lives-1
        
            drop_ele = random.choice([apple,egg,mango,guava,grapes,strawberry,watermelon])
        
            drop_element(xofdrop_ele, yofdrop_ele)
        


    
    
    
    
    #clock.tick(1000)
    #x=x+xchange
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                gameon=False
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_LEFT:
                    xchange=-15
                if event.key==pygame.K_RIGHT:
                    xchange=15
            if event.type==pygame.KEYUP:
                if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
                    xchange=0
                
        x=x+xchange
        if x > screen.get_width()-150 or x < 0 :
            xchange=0
        font = pygame.font.Font('fonts/font.otf', 40)
        score_color=(250, 250, 250)
    
        s = "Scores : " + str(score)
        text = font.render(s, 1, score_color)
        screen.blit(text, (100, 0))
    
        l = "Lives : " + str(lives)
        text = font.render(l, 1, score_color)
        screen.blit(text, (600,0))
    
        s = str(up_score)
        text = font.render(s, 1, score_color)
        screen.blit(text, (x+20, y-10))
    
        levelshow = "Level : " +str(level)
        text = font.render(levelshow, 1, score_color)
        screen.blit(text, (1100, 0))
    
    #pygame.display.update()
    
    #pygame.display.flip()
    
    #screen.blit(pygame.surface.text("wdcwc"), (100, 100))
    #pygame.display.flip()
        if lives == 0:
            
        #print("Game Over, Your score was: %s" % score)
            gameon = False
            #gameon= True
        basketey(x, y)
    
        drop_element(xofdrop_ele, yofdrop_ele)
        add_drop_element(xofadd_ele , yofadd_ele)
    
    
    #print("Scoree",score)
    #print("Livess",lives)
        pygame.display.update()

        clock.tick(60)
    if lives ==0:
        gameover.play()
        server_details = collection.find({"_id": loggedin_email})
        for detail in server_details:
            server_score = detail["score"]
            #print(detail["score"])
            #print(server_score["score"])
        if score >= server_score:
            server_score=score
            collection.update_one({"_id":loggedin_email},{ "$set": { "score":score } })
        toponserver=collection.find_one(sort=[("score", -1)])['User_Name_Register']
        #for detail in server_details:
         #   server_score = detail["score"]
        #print("Updated ",score)
        #    print("Email"+loggedin_email)
    #screen.blit(apple,(random.randrange(0,1000),20))

    while lives == 0:
        screen.blit(backgroundimg, (0, 0))
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_r:
                    xchange=-15    
                    lives=3
                    score=0
                    level=0
                    speed=4
                    yofadd_ele = 20
                    yofdrop_ele = 20
                    gameon=True
                if event.key==pygame.K_q:
                    pygame.quit()
                if event.key==pygame.K_l:
                    topscoreonserver = collection.find(sort=[("score", -1)])
                    # print("tototottototottoo"+str(topscoreonserver))
                    #for i in topscoreonserver:
                    #    print("Name ==== " + i["User_Name_Register"] + "  Score ====" + str(i["score"]))
                    leaderboardfunction()

        font = pygame.font.Font('fonts/font.otf', 85)
        gameoverresult = r"Game - Over "
        text = font.render(gameoverresult, 1, (250, 250, 250))
        screen.blit(text, (screen.get_width() // 2 - 250, 300))

        sc = "Your Current score : " + str(score) + "  High Score : " + str(server_score)
        font = pygame.font.Font('fonts/font.otf', 65)
        text = font.render(sc, 1, (250, 250, 250))
        screen.blit(text, (140, 400))


        re_qt="Press R to Restart, Q to Quit & L for Leader-Board"
        font = pygame.font.Font('fonts/font.otf', 55)
        text = font.render(re_qt, 1, (250, 250, 250))
        screen.blit(text, (80, 500))


        #print("Game Over, Your score was: %s" % score)  
        pygame.display.update()
        #print("sgsgssgs",score)
    
    
    
    
    
    
    
    