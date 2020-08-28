from tkinter import *
from Arya import *
import Arya
import sys
###########MAIN INITIALIZATION###################
Arya.personality = 50
root = Tk() #global blank window
Text_widget = Text(root, bd=7,font = ('Courier New Bold', '10'),fg='black',bg='snow')
Text_widget.tag_configure("mytag4", justify=CENTER)
Text_widget.insert(END,'Instructions\n \n',"mytag4")
Text_widget.insert(END,'Type in the Text Box (not Chat Screen)\n')
Text_widget.insert(END,'Press "enter" to send message into the text box\n')
Text_widget.insert(END,'Send message "end" or close window to end session\n \n')
Entry_widget = Entry(root, width="50", bg='snow',fg = 'black')

user_input=""
def main():
    root.title('Arya the ChatBot')
    root.geometry("520x630")
    root.configure(bg = 'dodger blue')


def textbox():
    label1 = Label(root, text="Enjoy your conversation with Arya!", fg = 'white', bg = 'dodger blue',
                   font = ('Courier New Bold', '16'))
    label1.grid()
    Text_widget.grid(column = 0, padx = 10, pady =10)
    scrollbar = Scrollbar(root,command =Text_widget.yview())
    scrollbar.grid(column = 1 , rowspan = 2, sticky = N+S+W)
    Text_widget['yscrollcommand'] = scrollbar.set
    entry_label = Label(root, text="Enter text message here:", fg='white', bg ='dodger blue',font =('Courier New Bold','14'))
    entry_label.grid()
    Entry_widget.grid(padx = 10, pady =10)
    # from here http://stackoverflow.com/questions/13832720/how-to-attach-a-scrollbar-to-a-text-widget

def clearscreen():
    Text_widget.delete(1.0, END)
    Text_widget.tag_configure("mytag4", justify=CENTER)
    Text_widget.insert(END,'Instructions\n \n',"mytag4")
    Text_widget.insert(END,'Type in the Text Box (not Chat Screen)\n')
    Text_widget.insert(END,'Press "enter" to send message into the text box\n')
    Text_widget.insert(END,'Send message "end" or close window to end session\n \n')

# display user input into text box
def getTextInput(str): 
    Text_widget.tag_configure("mytag3", background='lawn green')
    Text_widget.insert(END, str, "mytag3")
    Text_widget.insert(END, "\n")
    Text_widget.insert(END, "\n")
    Text_widget.yview_pickplace(END)  #Auto scroll to the end of the text
    # http://stackoverflow.com/questions/14824163/how-to-get-the-input-from-the-tkinter-text-box-widget


def sendTextOutput(str):
    output_string = str
    Chat_string = ' Arya: ' +output_string
    # this switches text to other side
    Text_widget.tag_configure("mytag2", justify='right')
    Text_widget.insert(END, ' ', "mytag2")
    Text_widget.tag_configure("mytag1", justify = 'right', background ='turquoise1')
    Text_widget.insert(END,Chat_string,"mytag1")
    Text_widget.insert(END, "\n")
    Text_widget.insert(END, "\n")
    Text_widget.yview_pickplace(END) #Auto scroll to the end of the text



def clear_button():
    button2 = Button(root, text="Clear Screen", command=clearscreen, width = 32, font =('Courier New Bold', '12'))
    button2.grid()
    #bg='black',fg='dodger blue', 

## get input from user
## must send to AI
def enterclick(event):
    Entry_widget.grid()

    saying =""

    while saying != "end" and saying != "quit" and saying != "exit":
        saying = Entry_widget.get()
        
        #print("this is the current: " + saying)
        user_input = 'User: ' + Entry_widget.get()
        getTextInput(user_input)
        Entry_widget.delete('0', 'end')
        posWord = any(substring in saying for substring in pos)
        negWord = any(substring in saying for substring in neg)
        if posWord == True:
            Arya.personality += 5
            displayLabelPercentage()
        if negWord == True:
            Arya.personality -= 5
            displayLabelPercentage()

        if saying == 'end' or saying == 'quit' or saying == 'exit':
            sendTextOutput("Goodbye")
            break

        elif 'time' in saying:
            Time = "It is " + time.strftime('%I:%M %p %Z on %b %d, %Y')
            sendTextOutput(Time)

        elif 'name' in saying:
            sendTextOutput("My name is Arya")

        elif 'Who are you' in saying or 'Who am I' in saying:
            if 'Who am I' in saying:
                if Arya.personality == 45 or Arya.personality == 55 or Arya.personality == 50:
                    sendTextOutput("You are a wanderer.")
                if Arya.personality > 55:
                    sendTextOutput("A wanderer and a " + Arya.random.choice(POS_END))
                if Arya.personality < 45:
                    sendTextOutput("A lost person and a " + Arya.random.choice(NEG_END2))
            if 'Who are you' in saying:
                if Arya.personality >= 45:
                    sendTextOutput("Well my name is Arya")
                    sendTextOutput("But I guess you could say I am something to help those who wander...")
                else:
                    sendTextOutput("Wouldn't you like to know bub...")
                    

        else:
            sendTextOutput(Arya.broback(saying))

        break;  # it wont read other enter click unless its outside
    if(saying == "end" or saying == "quit" or saying == "exit"): 
        raise SystemExit
        sys.exit()

## reads enter button
## calls method enter click
Entry_widget.bind("<Return>",enterclick)
Entry_widget.pack

def createLabelPercentage():
    empty = Label(root, fg = 'white', bg = 'dodger blue')
    empty.grid()
    percentage_label = Label(root, text="Personality Level ", fg='white', bg ='dodger blue',font =
    ('Courier New Bold','14'))
    percentage_label.grid()

def displayLabelPercentage():
    percentage_label_display = Label(root, text=Arya.personality, fg='white', bg ='dodger blue',font =
    ('Courier New Bold','14'))
    percentage_label_display.grid(row = 7)

def displayGoodPercentage():
    Arya.personality = 70
    percentage_label_display = Label(root, text=Arya.personality, fg='white', bg ='dodger blue',font =
    ('Courier New Bold','14'))
    percentage_label_display.grid(row = 7)
def displayBadPercentage():
    Arya.personality = 30
    percentage_label_display = Label(root, text=Arya.personality, fg='white', bg ='dodger blue',font =
    ('Courier New Bold','14'))
    percentage_label_display.grid(row = 7)


def displayNeutralPercentage():
    Arya.personality = 50
    percentage_label_display = Label(root, text=Arya.personality, fg='white', bg ='dodger blue',font =
    ('Courier New Bold','14'))
    percentage_label_display.grid(row = 7)


def goodButton():

    button3 = Button(root, text="Good", command = displayGoodPercentage, width=32, font=
    ('Courier New Bold', '12'))
    button3.grid()
    # bg='white', fg='dodger blue',

def neutralButton():

    button4 = Button(root, text="Neutral", command = displayNeutralPercentage,width=32, font=
    ('Courier New Bold', '12'))
    button4.grid()
    #bg='white', fg='dodger blue',

def badButton():
    button5 = Button(root, text="Bad", command = displayBadPercentage,width=32, font=
    ('Courier New Bold', '12'))
    button5.grid()
    #bg='white', fg='dodger blue', 


if __name__ == '__main__':
    main()
    textbox()
    clear_button()
    createLabelPercentage()
    displayLabelPercentage()
    goodButton()
    neutralButton()
    badButton()
    root.mainloop()
    