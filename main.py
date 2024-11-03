from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import socket
import requests
import mouse
from random import randint
from time import sleep


window = Tk()
window.title("Intruder v1.2")
window.geometry('800x600')

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
tabs.add(tab6, text="Mouse Sim")
tabs.pack(expand=1, fill='both')

tab7 = ttk.Frame(tabs)
tabs.add(tab7, text="Setting")
tabs.pack(expand=1, fill='both')

text1 = Label(tab1, text="You can save .onion URLs here")
text1.grid(column=0, row=0)

connection = sqlite3.connect('urls.db')
cur = connection.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS urls(
            id INTEGER PRIMARY KEY autoincrement, url TEXT, description TEXT);""")

# TAB 1 CONTENT

def saveurl(url, description):
    if len(url) > 4 and '.' in url:
        result = (url, description)
        cur.execute(r"INSERT INTO urls VALUES(NULL, ?, ?);", result)
        connection.commit()
        displayFields(len(returnDBContent()), returnDBContent())
        firstUrlField.insert(0, '')
        firstDescriptionField.insert(0, '')
    else:
        messagebox.showerror("Error", "URL lenght must be at least 4 symbols and contain '.'")


def returnDBContent():
    cur.execute("SELECT * FROM urls;")
    result = cur.fetchall()

    return result


def getEntryContent():
    url = firstUrlField.get()
    desc = firstDescriptionField.get()
    saveurl(url, desc)


def deleteEntry(index):
    cur.execute(f"DELETE FROM urls WHERE id={index};")
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

# TAB 1 CONTENT END

# TAB 2 CONTENT


def pingUrl(url):
    try:
        socket.setdefaulttimeout(5)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((url, 80))
    except OSError as error:
        return "Inactive"
    else:
        s.close()
        return "Active"


def checkAvailability():
    for i in returnDBContent():
        urlField = Label(tab2, text=i[1], borderwidth=2, relief="groove", width=30)
        urlField.grid(row=returnDBContent().index(i)+1, column=0)

        descField = Label(tab2, text=i[2], borderwidth=2, relief="groove", width=30)
        descField.grid(row=returnDBContent().index(i)+1, column=1)

        statusField = Label(tab2, text=pingUrl(i[1]), borderwidth=2, relief="groove", width=30)
        statusField.grid(row=returnDBContent().index(i)+1, column=2)


reloadBtn = Button(tab2, text="Reload URLs list", command=checkAvailability)
reloadBtn.grid(column=0, row=0)


# TAB 2 CONTENT END

# TAB 3 CONTENT

# TAB 3 CONTENT END

# TAB 4 CONTENT


def connectVPN():
    cntry = vpnField.get()
    j = 5
    result = []
    try:
        vpnServerListData = requests.get("http://www.vpngate.net/api/iphone/").text.replace(
            "\r", ""
        )
        freeServers = [line.split(",") for line in vpnServerListData.split("\n")]
        serverLabels = freeServers[1]
        serverLabels[0] = serverLabels[0][1:]
        freeServers = [srvrs for srvrs in freeServers[2:] if len(srvrs) > 1]
    except:
        print("Something is wrong! Cannot load the VPN server's data")
        exit(1)
    
    availableServers = [srvrs for srvrs in freeServers if cntry.lower() in srvrs[j].lower()]
    numOfServers = len(availableServers)
    result.append("We found " + str(numOfServers) + " servers for " + cntry + "\n")
    if numOfServers == 0:
        exit(1)

    supporteServers = [srvrs for srvrs in availableServers if len(srvrs[-1]) > 0]
    result.append("There are " + str(len(supporteServers)) + " servers that support OpenVPN\n")

    bestServer = sorted(
    supporteServers, key=lambda srvrs: float(srvrs[2].replace(",", ".")), reverse=True)[0]
    result.append("\n------------------Best server------------------\n")
    labelPair = list(zip(serverLabels, bestServer))[:-1]
    for (l, d) in labelPair[:4]:
        result.append(l + ": " + d + "\n")
    result.append(labelPair[4][0] + ": " + str(float(labelPair[4][1]) / 10 ** 6) + " MBps\n")
    result.append("Country: " + labelPair[5][1] + "\n")

    infoLbl = Label(tab4, width=60, text=result)
    infoLbl.grid(column=0, row=1)

    # print(result[4])


vpnField = Entry(tab4, width=60)
vpnField.grid(column=0, row=0)

connectVPNBtn = Button(tab4, text="Connect to VPN", command=connectVPN)
connectVPNBtn.grid(column=1, row=0)

# TAB 4 CONTENT END


# TAB 6 CONTENT


def simMouse():
    while True:
        mouse.move(randint(-350, 350), randint(-350, 350), absolute=False, duration=0.5)
        sleep(600)


moveBtn = Button(tab6, text="Start simulating", command=simMouse)
moveBtn.grid(column=1, row=0)


# TAB 6 CONTENT END

window.mainloop()
