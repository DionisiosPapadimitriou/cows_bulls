from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
import random,sys,string
import tkinter.scrolledtext as scrolled
from datetime import date
today = date.today()
global login_flag
login_flag=False

##close the application
def close_window():
	w.destroy()
	sys.exit()
	
##create the secret number
def num_gen():
    global a,tries
    tries=0;i=0
    a=[]
    while i <= 3:
        a.append(str(random.randint(0,9)))
        i+=1
    history.delete(0.0,END)
    output.delete(0.0,END)
    output.insert(END,"Secret number is now loaded! ")
    print(a)
# a=['1', '2', '3', '4' ] #this is for test reason

##compare user number with the random one
def check(x,y):
    cows=0;bulls=0;
    #Find Bulls
    while True:
        try:
            for i in range(len(y)):
                for j in range(len(y)):
                    if (x[i]==y[j]) and (x[j]!=y[j]):
                        bulls+=1
    #Find Cows
            for i in range(len(y)):
                if x[i] in y:
                    if x[i]==y[i]:
                        cows+=1
            history.insert(END,"\n"+str(user_num.get())+ " cows="+str(cows)+" bulls="+str(bulls))
            break
        except IndexError:#when input number has less digits than the secret number
            output.delete(0.0,END)
            output.insert(END,"Please give a correct number!\n")
            break
            
## Log in button pressed
def click2():
    global user,login_flag
    c=0
    output.delete(0.0,END)
    user=user_name.get()
    password=user_pass.get()
    with open('cb_users.txt') as r:
    	rfile=r.read()
    list_file=list(rfile.split('\n'))
    print(list_file)
    for item in list_file:#this is to count the lines in cb_users
    	c+=1
    #print(range(0,c))
    for i in range(c-1):
    	if user == list_file[i]  and password == list_file[i+1]:
    		messagebox.showinfo("Success", "succesful login")
    		login_flag=True
    		r.close()
    	if user == list_file[i] and password != list_file[i+1]:
  	  	messagebox.showinfo("Fail", "Unsuccesful login")
    		r.close()
    if user not in rfile:
  	  r.close()
  	  messagebox.showinfo("New user", "You are  registered as a new user.\nPlease remember your credentials for future use.")
  	  with open('cb_users.txt', 'a+') as f:
    		f.write(user+"\n")
    		f.write(password+"\n")
    		login_flag=True
    #print(login_flag)
    login.destroy()
    
##create highscore file
def highscore():

	with open("highscore.txt",'a+') as score:
		score.write(user +" "+  today.strftime("%d/%m/%Y") +" attempts: " + str(tries+1) + "\n")

def validate_num(num):
    for i in num:
        if i not in string.digits:
            return False
    return True

##When Try is pressed
def click():
	global a,tries, login_flag
	x=user_num.get()
	output.delete(0.0,END)
	if login_flag==True:
         if validate_num(x)==True:
            while True:
                try:
                    if len(x)>len(a):#when input number has more digits than the secret number
                        output.insert(END,"Please give number with " +str(len(a))+" digits")
                        break
                    elif list(x)!=a:
                        check(x,a)
                        #if not IndexError:
                        tries+=1
                        output.insert(END,"Please try again")
                        break
                    else:
                        output.insert(END,user + " you are the WINNER!!! You made it in "+str(tries+1)+" attempts")
                        login_flag=False
                        highscore()
                        break
                except NameError:#when secret number is not loaded
                    output.insert(END,"Please Load secret number first!")
                    break
         else:
             output.insert(END, "Please enter a valid number. Only digits 0-9")
	else:
		output.insert(END,"Please Log in first!")
	#print(str(login_flag) + " submit pressed")
				
				
##Login window
def log_in():
    global user_name,user_pass,login,history
    login=Tk()
    login.title("log in")
    user_name=Entry(login, width=10,bg="white")
    user_name.grid(row=0,column=1,columnspan=3)
    user_pass=Entry(login, width=10,bg="white")
    user_pass.grid(row=1,column=1,columnspan=3)
    Button(login,text="SUBMIT", width=10,command=click2).grid(row=2,column=1,columnspan=3)
    login.mainloop()

## Main window
w=Tk()
w.title("Cows & Bulls Game")
w.configure(bg="grey")
Label(w,text="Cows = correct digit in correct position\n"
             "Bulls = correct digit in wrong position",bg="grey",fg="white",font="none 12 bold").grid(row=0,column=1,columnspan=3)
Label(w,text="Guess the number: ",bg="grey",fg="black",font="none 12 italic").grid(row=2,column=0,columnspan=3)
user_num=Entry(w, width=10,bg="white")
user_num.grid(row=2,column=2,columnspan=3)
Button(w,text="TRY", width=6,command=click).grid(row=3,column=1,columnspan=3)
output=Text(w,width=40,height=2,wrap=WORD,bg="white")
output.grid(row=4,column=1,columnspan=3)
#history=Text(w,width=10,height=15,wrap=WORD,bg="white")
history = scrolled.ScrolledText(w, undo=True,width=20,height=15)
history.grid(row=0,column=5,sticky=E,padx=5,pady=5,rowspan=7)
Button(w,text="LOAD SECRET NUMBER", width=18,command=num_gen).grid(row=6,column=0,columnspan=3,sticky=W)
Button(w,text="EXIT", width=4,command=close_window).grid(row=6,column=2,columnspan=3,sticky=E)
Button(w,text="Log in",width=6,command=log_in).grid(row=7,column=1,columnspan=3)
w.mainloop()