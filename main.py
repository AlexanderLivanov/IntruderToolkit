from tkinter import *
from tkinter import ttk
import sqlite3


window = Tk()
window.title("Toririze v1.0")
window.geometry('800x500')

tabs = ttk.Notebook(window)

tab1 = ttk.Frame(tabs)
tabs.add(tab1, text="URL list")
tabs.pack(expand=1, fill='both')

tab2 = ttk.Frame(tabs)
tabs.add(tab2, text="Check availability")
tabs.pack(expand=1, fill='both')

tab3 = ttk.Frame(tabs)
tabs.add(tab3, text="Download TOR client")
tabs.pack(expand=1, fill='both')

tab4 = ttk.Frame(tabs)
tabs.add(tab4, text="VPN")
tabs.pack(expand=1, fill='both')

tab5 = ttk.Frame(tabs)
tabs.add(tab5, text="Proxy")
tabs.pack(expand=1, fill='both')

tab6 = ttk.Frame(tabs)
tabs.add(tab6, text="Setting")
tabs.pack(expand=1, fill='both')

text1 = Label(tab1, text="You can save .onion URLs here")
text1.grid(column=0, row=0)

connection = sqlite3.connect('urls.db')
cur = connection.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY autoincrement, url TEXT, description TEXT);""")


def saveurl(url, description):
    result = (url, description)
    cur.execute(r"INSERT INTO urls VALUES(NULL, ?, ?);", result)
    connection.commit()
    displayFields(len(returnDBContent()), returnDBContent())
    firstUrlField.insert(0, '')
    firstDescriptionField.insert(0, '')


def returnDBContent():
    cur.execute("SELECT * FROM urls;")
    result = cur.fetchall()
    
    return result


def getEntryContent():
    url = firstUrlField.get()
    desc = firstDescriptionField.get()
    saveurl(url, desc)


def deleteEntry(index):
    cur.execute(f"DELETE FROM urls WHERE id={index}")
    connection.commit()


def displayFields(count, res):
    for i in range(count):
        urlField = Entry(tab1, width=60)
        urlField.grid(column=0, row=i+1)
        urlField.insert(0, res[i][1])

        descriptionField = Entry(tab1, width=60)
        descriptionField.grid(column=1, row=i+1)
        descriptionField.insert(0, res[i][2])

        deleteBtn = Button(tab1, text=f"{i+1} (DELETE)", command=lambda i=i: deleteEntry(res[i][0]))
        deleteBtn.grid(column=2, row=i+1)


displayFields(len(returnDBContent()), returnDBContent())

firstUrlField = Entry(tab1, width=60)
firstUrlField.grid(column=0, row=0)

firstDescriptionField = Entry(tab1, width=60)
firstDescriptionField.grid(column=1, row=0)

saveBtn = Button(tab1, text="Save URLs", command=lambda: getEntryContent())
saveBtn.grid(column=2, row=0)

window.mainloop()