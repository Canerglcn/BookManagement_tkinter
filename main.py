from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
import sqlite3




root = Tk()
root.title("Book Management")
root.geometry("400x400")
root.eval('tk::PlaceWindow . center')



# .resize((100,90))
img=ImageTk.PhotoImage(Image.open("book.jpg").resize((100,90)))

imgLabel=Label(root,image=img).grid(row=0,column=0,columnspan=2)


'''
cursor.execute("""CREATE TABLE books (
                box_name char,
                name varchar(255),
                author varchar(255)
                
                )""")

'''

def update():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    record_id=select_box.get()

    conn.execute("""UPDATE books SET
        box_name = :box,
        name= :name,
        author= :author
        
        WHERE oid=:oid""",
     {
                'box':boxName_editor.get(),
                'name':name_editor.get(),
                'author':author_editor.get(),
                 'oid':record_id
                 })


    conn.commit()

    conn.close()

    editor.destroy()




def edit():


    record_id = select_box.get()
    if (len(record_id) == 0):
        messagebox.showerror("Error", "Please enter a book id")

    else:

        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()

        cursor.execute("Select * from books WHERE oid =" + record_id)
        records = cursor.fetchall()

        #Check that the Id exists in db
        if(len(records) == 0):
            messagebox.showerror("Error", "No book found")
        else:
            global editor
            editor = Tk()
            editor.title("Edit a Book")
            editor.geometry("400x400")

            global boxName_editor, name_editor, author_editor

            boxName_editor = Entry(editor, width=25)
            boxName_editor.grid(row=0, column=1, padx=5, pady=(10, 0))
            name_editor = Entry(editor, width=25)
            name_editor.grid(row=1, column=1, padx=5)
            author_editor = Entry(editor, width=25)
            author_editor.grid(row=2, column=1, padx=5)

            # create text box labels
            boxName_label = Label(editor, width=25, text="Box Name")
            boxName_label.grid(row=0, column=0, pady=(10, 0))
            name_label = Label(editor, width=25, text="Book Name")
            name_label.grid(row=1, column=0)
            author_label = Label(editor, width=25, text="Author")
            author_label.grid(row=2, column=0)

            for record in records:
                boxName_editor.insert(0, record[0])
                name_editor.insert(0, record[1])
                author_editor.insert(0, record[2])

            edit_btn = Button(editor, text="Save", command=update)
            edit_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=5, ipadx=150)

            select_box.delete(0, END)




def delete():

    if(len(select_box.get()) == 0):
        messagebox.showerror("Error", "Please enter a book id")
    else:
        conn = sqlite3.connect("books.db")

        conn.execute("DELETE from books WHERE oid=" + select_box.get())

        conn.commit()

        select_box.delete(0, END)

        conn.close()







def submit():

    if len(boxName.get())==0 or len(name.get())==0 or len(author.get())==0:
        messagebox.showerror("Error", "Please enter all fields")

    else:
        conn = sqlite3.connect("books.db")
        cursor = conn.cursor()

        conn.execute("INSERT INTO books VALUES (:b_name, :n_name, :a_author)",
                     {
                         'b_name': boxName.get(),
                         'n_name': name.get(),
                         'a_author': author.get(),
                     })

        # Clear Text Boxes
        boxName.delete(0, END)
        name.delete(0, END)
        author.delete(0, END)

        conn.commit()

        conn.close()



class Table:

    def __init__(self, root):

        # code for creating table
        for i in range(total_rows):
            for j in range(total_columns):
                self.e = Entry(root, width=15, fg='black',
                               font=('Arial', 10))

                self.e.grid(row=i+15, column=j)
                self.e.insert(END, records[i][j])




def showTable():
    conn = sqlite3.connect("books.db")
    cursor = conn.cursor()

    tableRoot = Tk()
    tableRoot.title("Books Table")
    tableRoot.geometry("600x800")

    heading_label=Label(tableRoot, text="Books Table",font=("Arial", 16, "bold"),padx=10,pady=10,fg="red" )
    heading_label.grid(row=0, column=0)

    head1_label=Label(tableRoot,text="BoxName",font=("Arial", 12, "bold"),padx=10,pady=5)
    head1_label.grid(row=1, column=0)
    head2_label = Label(tableRoot, text="Name",font=("Arial", 12, "bold"))
    head2_label.grid(row=1, column=1)
    head3_label = Label(tableRoot, text="Author",font=("Arial", 12, "bold"))
    head3_label.grid(row=1, column=2)
    head3_label = Label(tableRoot, text="ID",font=("Arial", 12, "bold"))
    head3_label.grid(row=1, column=3)



    cursor.execute("Select *, oid from books")
    global total_rows,total_columns,records
    records = cursor.fetchall()

    total_rows = len(records)
    total_columns=len(records[0])

    t=Table(tableRoot)

    conn.commit()

    conn.close()


#Create Text Boxes
boxName=Entry(root,width=25)
boxName.grid(row=3,column=1,padx=5,pady=(10,0))
name=Entry(root,width=25)
name.grid(row=4,column=1,padx=5)
author=Entry(root,width=25)
author.grid(row=5,column=1,padx=5)


select_box=Entry(root,width=25)
select_box.grid(row=8,column=1,padx=5,pady=5)


#create text box labels
boxName_label=Label(root,width=25,text="Box Name")
boxName_label.grid(row=3,column=0,pady=(10,0))
name_label = Label(root, width=25, text="Book Name")
name_label.grid(row=4, column=0)
author_label = Label(root, width=25, text="Author")
author_label.grid(row=5, column=0)


delete_box_label=Label(root, text="ID Number")
delete_box_label.grid(row=8, column=0,pady=5)



submit_btn = Button(root, text="Add Book", command=submit)
submit_btn.grid(row=6, column=0, columnspan=2, padx=10, pady=10, ipadx=150)


show_btn=Button(root, text="Show Books", command=showTable)
show_btn.grid(row=7, column=0, columnspan=2, padx=10, pady=5, ipadx=145)

delete_btn=Button(root, text="Delete Book", command=delete)
delete_btn.grid(row=10, column=0, columnspan=2, padx=10, pady=5, ipadx=145)

edit_btn=Button(root, text="Edit Book", command=edit)
edit_btn.grid(row=9, column=0, columnspan=2, padx=10, pady=5, ipadx=150)


root.mainloop()


