from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import requests
import json
import mysql.connector


root = Tk()
root.title("Currency Converter")
root.geometry("730x550")
root.iconbitmap(r"exchange.ico")
root.option_add( "*font", "CascadiaMono 14" )

def ShowConnectionWarning():
   messagebox.showwarning("WARNING","Not able to connect to the internet!")
#API connection Here
try:
    url = 'https://api.exchangerate-api.com/v4/latest/USD'
    data = requests.get(url).text
    print("Api connection successfull")
    dataJSON = json.loads(data)
    dataRates = dataJSON["rates"]
    f = open('currency.json','w')
    f.write(data)
    f.close()

except:
   print('Api connection failed')
   ShowConnectionWarning()
   openfile = open('currency.json')
   datajson = json.load(openfile)
   dataRates = datajson["rates"]


global conversion_rate
conversion_rate = 0
global count
count = 0
global count1
count1 = 0

#mysql workings are here
def SaveInDatabase(choice1,choice2,amount,converted_amount,conversion_rate):
    global count
    count+=1
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="@99388849Gv",database = 'mysql')
    cursor = mydb.cursor()
    cursor.execute('insert into conversion(num,from_currency,to_currency,amount,converted_amount,conversion_rate) values(%s,%s,%s,%s,%s,%s)',(count,choice1,choice2,amount,converted_amount,conversion_rate))
    mydb.commit()

def SetPreValues():
   prevalue = 1
   drop1_entry.insert(0,str(prevalue))
   convertit()

def ShowError1():
   messagebox.showerror("Input Error","Please give one input !")

def ShowError2():
   messagebox.showerror("Input Error","Please give valid input !")

def Clear_all():
   drop1_entry.delete(0,END)
   drop2_entry.delete(0,END)
   third_entry.delete(0,END)

def ShowData(listbox):
    mydb = mysql.connector.connect(host="localhost",user="root",passwd="@99388849Gv",database = 'mysql')
    cursor = mydb.cursor()
    cursor.execute('select * from conversion')
    records = cursor.fetchall()
    global count1
    num = records[count1][0]
    from_currency = records[count1][1]
    to_currency = records[count1][2]
    amount = records[count1][3]
    converted_amount = records[count1][4]
    conversion_rate = records[count1][5]

    listbox.insert('','end',values=(num,from_currency,to_currency,amount,converted_amount,conversion_rate))
    count1 += 1
    mydb.close()
  

    

def ClearTable():
   mydb = mysql.connector.connect(host="localhost",user="root",passwd="@99388849Gv",database = 'mysql')
   cursor = mydb.cursor()
   cursor.execute('delete from conversion')
   mydb.commit()

               
#Retriving data function
def convertit():
   #Getting the values of option menu
   global conversion_rate
   str1 = drop1_clicked1.get()
   str2 = drop2_clicked2.get()
   s1 = slice(3)
   choice1 = str1[s1]
   choice2 = str2[s1]
  #getting the values of entries
   value1 =drop1_entry.get()
   value2 =drop2_entry.get()
  
   if (value1 == "" and value2 == ""):
      ShowError1()
      third_entry.delete(0,END)

   elif (value1.isnumeric() == False and value2.isnumeric() == False):
      ShowError2()
      Clear_all()

   elif(value1 == ""):
      
      to_currency = choice1
      from_currency = choice2
      amount = float(value2)
      conversion_rate = round((dataRates[to_currency]/dataRates[from_currency]),4)
      third_entry.delete(0,END)
      third_entry.insert(0,str(conversion_rate))
      converted_amount = round(float(amount * conversion_rate),1)
      drop1_entry.insert(0,converted_amount)
      SaveInDatabase(choice2,choice1,amount,converted_amount,conversion_rate)
      ShowData(listbox)

   elif(value2 == ""):
    
      to_currency = choice2
      from_currency = choice1
      amount = float(value1)
      conversion_rate = round((dataRates[to_currency]/dataRates[from_currency]),2)
      third_entry.delete(0,END)
      third_entry.insert(0,str(conversion_rate))
      converted_amount = round(float(amount * conversion_rate),1)
      drop2_entry.insert(0,converted_amount)
      SaveInDatabase(choice1,choice2,amount,converted_amount,conversion_rate)
      ShowData(listbox)
      
   else:
      from_currency = choice1
      to_currency = choice2
      amount = float(value1)
      conversion_rate = round((dataRates[to_currency]/dataRates[from_currency]),2)
      converted_amount = round(float(amount * conversion_rate),1)
      preconversion_rate = third_entry.get()
      if(float(value2) == converted_amount and float(preconversion_rate) == conversion_rate):
         return
      else:
         drop1_entry.delete(0,END)
         drop2_entry.delete(0,END)

#Heading
head_label = Label(root,text='CURRENCY CONVERTER',width=40,fg='white',bg='black',font=("Roboto Mono",22))
head_label.pack(pady=10)    
      
#Create Tabs
my_notebook = ttk.Notebook(root)
my_notebook.pack(pady=20)

#Creating two frames
frame1 = Frame(my_notebook,width=680,height=440)
frame2 = Frame(my_notebook,width=680,height=440)

frame1.pack(fill='both',expand = 1)
frame2.pack(fill='both',expand = 1)

#Adding tabs
my_notebook.add(frame1,text="Conversion")
my_notebook.add(frame2,text="Previous Conversions")

# creating label frame for currency
first_frame = LabelFrame(frame1,text="Select Currency")
first_frame.pack(pady=35)

#clear button functions
def clear_entry1():
   drop1_entry.delete(0, END)

def clear_entry2():
   drop2_entry.delete(0, END)

def clear_thirdentry():
   third_entry.delete(0, END)

#Options for option menu
options = [

   "BRL Brazilian Real",
   "BYN Belarus Ruble",
   "KHR Cambodian Riel",
   "CAD Canadian Dollar",
   "CNY Chinese Yuan",
   "CLP Chilean Peso",
   "EUR Euro",
   "INR Indian Rupee",
   "JPY Japanese Yen",
   "MXN Mexican peso",
   "NPR Nepalese Rupee",
   "PKR Pakistan Rupee",
   "RUB Russian Ruble",
   "SAR Saudi Riyal",
   "SGD Singapore Dollar",
   "CHF Swiss Franc",
   "THB Thai Baht",
   "AED UAE Dirham",
   "USD US Dollar",
]

#Elements of frame1

#setting default value for option menus
drop1_clicked1 = StringVar()
drop1_clicked1.set(options[18])

drop2_clicked2 = StringVar()
drop2_clicked2.set(options[7])

#setting the width of option menu to the max width of options
menu_width = len(max(options, key=len))

#first drop
drop1 = OptionMenu(first_frame,drop1_clicked1,*options)
drop1.config(width=menu_width)
drop1.grid(row=1,column=0,padx=10,pady=10)

#first drop entry
drop1_entry = Entry(first_frame,font=("Segoe UI",15),fg="blue")
drop1_entry.grid(row=1,column=1,padx=30)

#second drop
drop2 = OptionMenu(first_frame,drop2_clicked2,*options)
drop2.config(width=menu_width)
drop2.grid(row=2,column=0,padx=10,pady=10)

#second drop entry
drop2_entry = Entry(first_frame,font=("Segoe UI",15),fg="blue")
drop2_entry.grid(row=2,column=1,padx=30)

#clear buttons in frame1

#clear buttons image
clearbtn_img = PhotoImage(file="erase.png")
#for first entry
clear_btn1=Button(first_frame,image=clearbtn_img ,borderwidth=0, command=clear_entry1)
clear_btn1.grid(row=1,column=2,padx=5,pady=10)

#for second entry
clear_btn2=Button(first_frame,image=clearbtn_img ,borderwidth=0 , command=clear_entry2)
clear_btn2.grid(row=2,column=2,padx=5,pady=10)

#for third entry
clear_btn3=Button(first_frame,image=clearbtn_img ,borderwidth=0 , command = clear_thirdentry)
clear_btn3.grid(row=3,column=2,padx=5,pady=10)


label1 = Label(first_frame ,text = "CONVERSION RATE",font=('CascadiaMono 16'),borderwidth=3, relief="sunken",width=21)
label1.grid(row = 3,column=0,pady=14)

third_entry = Entry(first_frame,font=("Segoe UI",15),fg="blue")
third_entry.grid(row=3,column=1,padx=30)

convert_btn = Button(first_frame,text="CONVERT",command=convertit,bg='#2a9d8f',fg='#ffffff',width=12,font=("CascadiaMono 15"))
convert_btn.grid(row=4,column=1,pady = 30)

Clearall_btn = Button(first_frame,text="CLEAR ALL",command=Clear_all,bg='#d62828',fg='#ffffff',width=12,font=("CascadiaMono 15"))
Clearall_btn.grid(row=4,column=0,pady = 30)

#Image
logo_img = PhotoImage(file='exchange.png')
logo_label = Label(image=logo_img)
logo_label.place(x=650,y=70)

#background image adding
path = "coins2.jpg"
img = ImageTk.PhotoImage(Image.open(path))
panel = Label(image = img)
panel.pack(side="right",fill="both", expand = True)

path = "money.jpg"
img2 = ImageTk.PhotoImage(Image.open(path))
panel = Label(image = img2)
panel.pack(side="bottom",fill="both", expand = True)





# using treeview to show tabular data
cols = ('num','From Currency','To Currency','Amount','Converted Amount','Conversion Rate') 
listbox = ttk.Treeview(frame2,columns=cols,show='headings')

for col in cols:
    listbox.heading(col,text=col)
    listbox.grid(row=1,column=0,columnspan=2)
    listbox.pack(pady = 40)



#Setting width of every column in tree view
listbox.column("num", width = 50, anchor ='center')
listbox.column("From Currency", width = 115, anchor ='center')
listbox.column("To Currency", width = 115, anchor ='center')
listbox.column("Amount", width = 115, anchor ='center')
listbox.column("Converted Amount", width = 125, anchor ='center')
listbox.column("Conversion Rate", width = 125, anchor ='center')


ClearTable()
SetPreValues()

root.mainloop()