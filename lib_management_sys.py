from tkinter import *
from tkinter.font import BOLD
from tkinter import messagebox
import sqlite3
from tkcalendar import Calendar
import datetime
from datetime import timedelta,date #for adding perticular no of days to your date
from PIL import ImageTk,Image
from tkinter import ttk

#current date
current_date = datetime.datetime.now()


root = Tk()
root.title("Liberary Management")
photo = PhotoImage(file = "C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/libray_logo.png")
root.iconphoto(True, photo)
root["background"]="#FFFFC1"
root.resizable(False,False)

#creating database tabel for the Books record
conn = sqlite3.connect('C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/lib_books_database.db')
c = conn.cursor()

try:
  c.execute("""CREATE TABLE issued_books(
                    Book_name text,
                    Student_name text,
                    Student_id integer,
                    Date TIMESTAMP
  )""")
  print("Database tabel created")
except:
  print("Database tabel allready created")

conn.commit()
conn.close()

#function add books issued to data base
def submit():
  if bname_entry.get() != "":
    conn = sqlite3.connect("C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/lib_books_database.db")

    c = conn.cursor()

    c.execute("INSERT INTO issued_books VALUES(:bname,:sname,:sid,:date)",
              {
                'bname' : bname_entry.get().capitalize(),
                'sname' : sname_entry.get().capitalize(),
                'sid' : sid_entry.get(),
                'date' : cal.get_date()
              })
    conn.commit()
    conn.close()
    messagebox.showinfo("showinfo", f"Book issued sucessfully to {sname_entry.get()}.")

  else:
    messagebox.showinfo("showinfo", f"empty")

  bname_entry.delete(0, END)
  sname_entry.delete(0, END)
  sid_entry.delete(0, END)

#remove book from that database
def remove_book():
  conn = sqlite3.connect('C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/lib_books_database.db')
  c = conn.cursor()
  #select item into list from treeview
  selected_item = my_tree.selection() #giver u selected row no.
  for selected in selected_item:
    #selecting values of that selected row
    values = my_tree.item(selected, 'values')

    c.execute("DELETE FROM issued_books WHERE oid = "+ values[4])
    #delete it from the screen
    my_tree.delete(selected)
    
  conn.commit()
  conn.close()

#print all books in window
def print_all_books():
  conn = sqlite3.connect("C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/lib_books_database.db")
  c = conn.cursor()

  c.execute("SELECT *,oid FROM issued_books")
  records=c.fetchall()

  show_books = Tk()
  show_books.title("All Issued books")
  show_books["background"]="#FFFFC1"
  show_books.geometry("710x300")
  show_books.resizable(False,False)
  
  #styling tree view
  style =ttk.Style(show_books)

  style.theme_use("clam")

  style.configure("Treeview.Heading",background="#FFD2A5", foreground="black")
  style.map('Treeview',background=[('selected', '#8A79AF')])  

  #creating a frame then adding scrolebar and tree into it
  tree_frame = Frame(show_books)
  tree_frame.pack(padx=10,pady=10,anchor=W)

  tree_scroll = Scrollbar(tree_frame)
  tree_scroll.pack(side=RIGHT,fill=Y)

  global my_tree

  my_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
  my_tree.pack()

  tree_scroll.config(command=my_tree.yview)


  my_tree['columns'] = ("Book Name","Student Name","Student ID","Date","Book ID")

  my_tree.column("#0",width = 0,stretch=NO)
  my_tree.column("Book Name",anchor=W, width=200)
  my_tree.column("Student Name",anchor=W, width=140)
  my_tree.column("Student ID",anchor=CENTER, width=100)
  my_tree.column("Date",anchor=CENTER, width=140)
  my_tree.column("Book ID",anchor=W, width=83)

  my_tree.heading("#0",text="",anchor=W)
  my_tree.heading("Book Name",text="Book Name",anchor=W)
  my_tree.heading("Student Name",text="Student Name",anchor=W)
  my_tree.heading("Student ID",text="Student ID",anchor=CENTER)
  my_tree.heading("Date",text="Book Issue Date",anchor=CENTER)
  my_tree.heading("Book ID",text="Book ID",anchor=W)

  count=0
  for record in records:
    my_tree.insert(parent='', index='end', iid=count,text="",values=(record[0],record[1],record[2],record[3],record[4]))
    count=count+1
  
  conn.commit()
  conn.close()

  del_label = Label(show_books,text="Remove Selected Books from the Database:",font=('Arial',13,BOLD),bg="#FFFFC1")
  del_label.pack(padx=10,side=LEFT,anchor=CENTER)
  del_button = Button(show_books,text="Remove",command=remove_book,font=('Arial',13,BOLD),width=10,bg="#F90716",fg="white")
  del_button.pack(padx=10,pady=(0,10),side=LEFT,anchor=CENTER)


  show_books.mainloop()

#open new window to add books
def issue_book():
  issue = Tk()
  issue.title('Issue Book')
  issue.geometry('300x500')
  issue["background"]="#FFFFC1"
  issue.resizable(False,False)

  global bname_entry
  global sname_entry
  global sid_entry
  global cal

  #heading label
  h_label = Label(issue,text="ISSUE BOOK",font=('Arial',25,BOLD),bg="#FFFFC1")
  h_label.grid(row=0,padx=(20,0),pady=10)
  #book name entry
  t_book = Label(issue,text="Enter Book name :",bg="#FFFFC1")
  t_book.grid(row=2,sticky='w',padx=10)
  bname_entry = Entry(issue,width=45)
  bname_entry.grid(row=3,padx=10,pady=(0,10))
  #student name entry
  t_student = Label(issue,text="Enter Student name :",bg="#FFFFC1")
  t_student.grid(row=4,sticky='w',padx=10)
  sname_entry = Entry(issue,width=45)
  sname_entry.grid(row=5,padx=10,pady=(0,10))
  #studentid entry
  t_studentid = Label(issue,text="Enter Student ID:",bg="#FFFFC1")
  t_studentid.grid(row=6,sticky='w',padx=10)
  sid_entry = Entry(issue,width=22)
  sid_entry.grid(row=7,padx=10,pady=(0,10),sticky='w')
  #date
  t_date = Label(issue,text="Choose Date book issued :",bg="#FFFFC1")
  t_date.grid(row=8,sticky='w',padx=10)

  cal = Calendar(issue,selectmode = 'day',year = current_date.year, month = current_date.month,day = current_date.day,background="#D38CAD", foreground='white')
  cal.grid(row=9,padx=10,pady=(0,10),sticky='w')
  #issue button
  isu_button = Button(issue,text="Issue Book",font=('Arial',12,BOLD),width=22,command=submit,bg="#8A79AF",fg="white")
  isu_button.grid(row=10,padx=10,pady=22)


  issue.mainloop()

#delaulters details window
def defaulters():
  def_window = Tk()
  def_window.title("Defaulters")
  def_window["background"]="#FFFFC1"

  def_label = Label(def_window,text="DEFAULTERS LIST",font=('Arial',31,BOLD),bg="#FFFFC1").pack(padx=10,pady=(10,0),anchor=CENTER)


  conn = sqlite3.connect("C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/lib_books_database.db")
  c = conn.cursor()

  c.execute("SELECT *,oid FROM issued_books")
  records=c.fetchall()

  #styling tree view
  style =ttk.Style(def_window)

  style.theme_use("clam")

  style.configure("Treeview.Heading",background="#FFD2A5", foreground="black")
  style.configure("Treeview", background="#FE4141",fg="#FFFFFF")
  style.map('Treeview',background=[('selected', '#8A79AF')])  

  #creating a frame then adding scrolebar and tree into it
  tree_frame = Frame(def_window)
  tree_frame.pack(padx=10,pady=10,anchor=CENTER)

  tree_scroll = Scrollbar(tree_frame)
  tree_scroll.pack(side=RIGHT,fill=Y)

  def_tree = ttk.Treeview(tree_frame,yscrollcommand=tree_scroll.set,selectmode="extended")
  def_tree.pack()

  tree_scroll.config(command=def_tree.yview)


  def_tree['columns'] = ("Book Name","Student Name","Student ID","Date","Book ID","Return Date","No.of Day Extended")

  def_tree.column("#0",width = 0,stretch=NO)
  def_tree.column("Book Name",anchor=W, width=200)
  def_tree.column("Student Name",anchor=W, width=140)
  def_tree.column("Student ID",anchor=CENTER, width=100)
  def_tree.column("Date",anchor=CENTER, width=140)
  def_tree.column("Book ID",anchor=W, width=83)
  def_tree.column("Return Date",anchor=CENTER, width=140)
  def_tree.column("No.of Day Extended",anchor=W, width=100)

  def_tree.heading("#0",text="",anchor=W)
  def_tree.heading("Book Name",text="Book Name",anchor=W)
  def_tree.heading("Student Name",text="Student Name",anchor=W)
  def_tree.heading("Student ID",text="Student ID",anchor=CENTER)
  def_tree.heading("Date",text="Book Issue Date",anchor=CENTER)
  def_tree.heading("Book ID",text="Book ID",anchor=W)
  def_tree.heading("Return Date",text="Book Issue Date",anchor=CENTER)
  def_tree.heading("No.of Day Extended",text="No. of Day Extended",anchor=W)

  co=0

  for record in records:

    #converting the string date in date and tym module accesabel form 
    date_1 = datetime.datetime.strptime(record[3], "%m/%d/%y")
    #it return returndate whivh is day of issued book +7 days
    Return_date = str(date_1 + timedelta(days=7)).split()
    print(Return_date)
    #calulating no of days (book has been issued)
    new_date = str(current_date - date_1).split()
    print(new_date)

    if int(new_date[0]) >= 7:

      def_tree.insert(parent='', index='end', iid=co,text="",values=(record[0],record[1],record[2],record[3],record[4],Return_date[0],new_date[0]))
      co=co+1




  conn.commit()
  conn.close()


  def_window.mainloop()


button_frame = Frame(root,bg="#FFFFC1")
button_frame.grid(row=1,column=1,padx=10,pady=10,sticky=NS)

text_label = Label(button_frame,text="CITY LIBRARY",font=('Arial',31,BOLD),bg="#FFFFC1",fg="#5B1876").pack(anchor=N)

#button to run issue book function
issue_Button = Button(button_frame, text="Issue Book", command=issue_book,bg="#FFD2A5",height=2,width=22,font=('',13,BOLD)).pack(padx=40,pady=(40,0))

print_books = Button(button_frame,text="Print All Books",command=print_all_books,bg="#FFD2A5",height=2,width=22,font=('Arial',13,BOLD)).pack(padx=20,pady=31)

def_button = Button(button_frame,text="Defaulters detail",command=defaulters,bg="#FFD2A5",height=2,width=22,font=('Arial',13,BOLD)).pack()

#ADD IMAGE IN MAIN PAGE
image_open = Image.open("C:/Users/jasmeet singh/.vscode/python_program/tkinter_programs/amazing-libraries-5__880.jpg")
image_resize = image_open.resize((400,400))
book_image = ImageTk.PhotoImage(image_resize)

image_frame = Frame(root)
image_frame.grid(row=1,column=2,sticky=NE)

img_label = Label(image_frame,image=book_image).pack()

root.mainloop()