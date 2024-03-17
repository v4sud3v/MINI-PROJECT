from tkinter import*

def screen(i):
    e.insert(END,i)

a=[]
s=""
window=Tk()
root=LabelFrame(window,border=10,borderwidth=10).grid(row=0,column=0)
window.title("calculator")

#root.geometry("250x350")
def button_click(sign):
    global s
    a.append(float(e.get()))
    e.delete(0, 'end')
    if len(a) == 2:
        r2=a.pop()
        r1=a.pop()
        if s=="+":
            r1+=r2
        elif s=="-":
            r1-=r2
        elif s=="*":
            r1*=r2
        elif s=="/":
            r1/=r2
        e.insert(END,r1)
    s=sign

 
def clear_screen():
    e.delete(0, 'end')

e=Entry(root,width=35,border=3,bg="grey",borderwidth=5)
e.grid(row=0,column=0,columnspan=4)
B7=Button(root,text="     7     ",padx=15,pady=15,command=lambda:screen(7),bg="black",borderwidth=2,fg="white")
B8=Button(root,text="     8     ",padx=15,pady=15,command=lambda:screen(8),bg="black",borderwidth=2,fg="white")
B9=Button(root,text="     9     ",padx=15,pady=15,command=lambda:screen(9),bg="black",borderwidth=2,fg="white")  
B4=Button(root,text="     4     ",padx=15,pady=15,command=lambda:screen(4),bg="black",borderwidth=2,fg="white")
B5=Button(root,text="     5     ",padx=15,pady=15,command=lambda:screen(5),bg="black",borderwidth=2,fg="white")
B6=Button(root,text="     6     ",padx=15,pady=15,command=lambda:screen(6),bg="black",borderwidth=2,fg="white")  
B1=Button(root,text="     1     ",padx=15,pady=15,command=lambda:screen(1),bg="black",borderwidth=2,fg="white")
B2=Button(root,text="     2     ",padx=15,pady=15,command=lambda:screen(2),bg="black",borderwidth=2,fg="white")
B3=Button(root,text="     3     ",padx=15,pady=15,command=lambda:screen(3),bg="black",borderwidth=2,fg="white")

B0=Button(root,text="                  0                     ",padx=9,pady=15,command=lambda:screen(0),bg="black",fg="white")

B7.grid(row=1,column=0)
B8.grid(row=1,column=1)
B9.grid(row=1,column=2)

B4.grid(row=2,column=0)
B5.grid(row=2,column=1)
B6.grid(row=2,column=2)

B1.grid(row=3,column=0)
B2.grid(row=3,column=1)
B3.grid(row=3,column=2)

B0.grid(row=4,column=0,columnspan=2)
plu=Button(root,text="  +  ",pady=15,command=lambda:button_click("+")).grid(row=1,column=3)
min=Button(root,text="  -   ",pady=15,command=lambda:button_click("-")).grid(row=2,column=3)
mul=Button(root,text="  *   ",pady=15,command=lambda:button_click("*")).grid(row=3,column=3)
div=Button(root,text="  /   ",pady=15,command=lambda:button_click("/")).grid(row=4,column=3)
equ=Button(root,text="  =  ",pady=15,padx=23,command=lambda:button_click("=")).grid(row=4,column=2)
clear=Button(root,text="clear",command=clear_screen)

window.mainloop()