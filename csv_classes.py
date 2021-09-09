import pandas as pd
from PIL import Image
import os

class message:
    def __init__(self,id,text,file= None):
        self.id = id
        self.text = text
        self._files = []
        self._files.append(file)

class user:
    def __init__(self,name,password,logged_in=False,signed_up=True):
        self.name = name
        self.password = password
        self.logged_in = logged_in
        self.signed_up = signed_up
        self.inbox = None
        self.sent = None

    def send(self,to_user,message):
        all_messages = pd.read_csv("Messages.csv") 
        details = {"ID":message.id,"To":to_user.name,"From":self.name,"Text":message.text}
        all_messages = all_messages.append(details,ignore_index=True)
        all_messages.to_csv("Messages.csv",index=False)

        print(f"Message sent from {self.name} to {to_user.name}")

    def view_inbox(self):
        all_messages = pd.read_csv("Messages.csv")
        all_received_messages = [m for m in all_messages[all_messages['To']==self.name]['Text']]
        print(all_received_messages[::-1])
        return all_received_messages[::-1]

    def view_sent(self):
        all_messages = pd.read_csv("Messages.csv")
        all_sent_messages = [m for m in all_messages[all_messages['From']==self.name]['Text']]
        print(all_sent_messages[::-1])
        return all_sent_messages[::-1]


# adding data to the Messages.csv file , which will contain all messages
def add_to_messages(subject,to,username,message,time_sent,filename,file_loc=None):
    if file_loc==None:
        temp_message = pd.DataFrame()
        new_message = {'ID':subject, 'To':to , 'From':username , 'Message':message,"Time":time_sent}
        temp_message = temp_message.append(new_message,ignore_index=True)
        temp_message.to_csv(filename,mode='a',index=False,header=False)
    else:
        temp_message = pd.DataFrame()
        new_message = {'ID':subject, 'To':to , 'From':username , 'Message':message,"Time":time_sent,"File":file_loc}
        temp_message = temp_message.append(new_message,ignore_index=True)
        temp_message.to_csv(filename,mode='a',index=False,header=False)

# function to clear messages of inbox and sent 
def clear_inbox_or_sent(username,filename,to_or_from):

    all_messages = pd.read_csv(filename)
    my_messages = all_messages[all_messages[to_or_from]==username]
    my_indices = my_messages.index

    all_messages.drop(my_indices,axis=0,inplace=True)
    all_messages.to_csv(filename,index=False)
    print(all_messages)
    if to_or_from=='From':
        return "Sent messages cleared<br>"
    elif to_or_from=='To':
        return "Inbox cleared<br>"

# function to view inbox or sent messages
def view_inbox_or_sent(username,filename,to_or_from):

    response=""
    username= username
    
    if to_or_from=='To':
        sent_or_received = 'sent'
        color = 'red'
        check_user = 'From'
    elif to_or_from=='From':
        sent_or_received = 'received'
        color = 'green'
        check_user = 'To' 
    # collecting messages from dataframe that have From or To as username
    all_messages=pd.read_csv(filename)
    my_sent_messages = all_messages[all_messages[check_user]==username]

    #my_sent_messages['Time'] = pd.to_datetime(my_sent_messages['Time'])
    my_sent_messages.loc['Time'] = pd.to_datetime(my_sent_messages['Time'])
    my_sent_messages.sort_values(by='Time',inplace=True,ascending=False)
    
    # this will contain list of tuples of (message content, receiver_or_sender , time , subject , files_attached)
    messages = [(msg,to_of,tm,id,fl) for (msg,to_of,tm,id,fl) in zip(my_sent_messages.Message,my_sent_messages[to_or_from],my_sent_messages.Time,my_sent_messages.ID,my_sent_messages.File)]
    for msg,to_of,tm,sub,fl in messages:
        # if fl is nan, it will not be equal to itself
        if fl != fl:
            response+=f'''<div style="border:2px;border-style:solid;border-color:black;color:{color};"><h4> {to_or_from} {to_of}:<br>Subject: {sub}<br><br><div style="color:orange; border:2px;border-style:solid;border-color:white;margin-left:5px;margin-right:5px;">{msg}</div><br><br>At:{tm} </h4></div><br>'''
        else:
            if fl.endswith(".txt"):
                f = open(fl,'r')
                response+=f'''<div style="border:2px;border-style:solid;border-color:black;color:{color};"><h4>You have {sent_or_received} a text file.<br><br><b>Content:<br><br></b><div style="color:orange; border:2px;border-style:solid;border-color:white;margin-left:5px;margin-right:5px;">{f.read()}</div></h4></div><br>'''
            elif fl.endswith((".jpg",".png",".jpeg",".jfif")):
                img = Image.open(fl)
                img1 = img.save(f"static/images/{os.path.basename(fl)}")
                base = os.path.basename(fl)
                response+=f'''<div style="border:2px;border-style:solid;border-color:black;color:{color};"><h4> {to_or_from} {to_of}:<br>Subject: {sub}<br><br><div style="color:orange; border:2px;border-style:solid;border-color:white;margin-left:5px;margin-right:5px;">{msg}<br>At:{tm} </div></h4><br>'''
                response+=f'''You have {sent_or_received} {base}<br><img src="/static/images/{base}" width="200" height="200" /></div><br>'''
    return response

