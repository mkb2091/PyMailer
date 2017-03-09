from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
import email.utils
import smtplib

import subprocess
import platform
import re

from tkinter import filedialog
import tkinter.ttk as ttk
import tkinter as tk

def MXlookup(domain):
    try:
        if platform.system()=='Windows':
            data=subprocess.getoutput('nslookup -q=mx '+domain)
            data=re.findall('MX preference = (.*?), mail exchanger = (.*?)\n',
                            data)
            return min([int(i[0]), i[1]] for i in data)[1]
        elif platform.system()=='Linux':
            data=subprocess.getoutput('host '+domain)
            data=re.findall('mail is handled by (.*?) (.*?)\n', data+'\n')
            return min([int(i[0]), i[1]] for i in data)[1]
    except ValueError:
        pass
    return domain
class AttachmentManager(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        ttk.Label(self, text='Attachments').pack()
        self.attachments=[]
        self.attachment_labels=[]
        ttk.Button(self, text='Clear', command=self.clear).pack(side='bottom')
        ttk.Button(self, text='Add', command=self.add).pack(side='bottom')
    def add(self):
        d=filedialog.askopenfilename()
        if d:
            self.attachments.append(d)
            self.attachment_labels.append(ttk.Label(self, text=d))
            self.attachment_labels[-1].pack(side='bottom')
    def clear(self):
        for i in self.attachment_labels:
            i.destroy()
        self.attachments=[]
        self.attachment_labels=[]
    def get_attachments(self):
        return self.attachments
class PyMailer(ttk.Frame):
    def __init__(self, master=None):
        ttk.Frame.__init__(self, master)
        ttk.Label(self, text='To:').pack(anchor='sw')
        self.rcpttos=tk.Text(self, height=5)
        self.rcpttos.pack(anchor='w')
        ttk.Label(self, text='From address:').pack(anchor='sw')
        self.fromaddr=tk.Text(self, height=1)
        self.fromaddr.pack(anchor='w')
        ttk.Label(self, text='From name:').pack(anchor='sw')
        self.fromname=tk.Text(self, height=1)
        self.fromname.pack(anchor='w')
        ttk.Label(self, text='Subject:').pack(anchor='sw')
        self.subject=tk.Text(self, height=1)
        self.subject.pack(anchor='w')
        ttk.Label(self, text='Body:').pack(anchor='sw')
        self.body=tk.Text(self, height=10)
        self.body.pack(anchor='w')
        self.attachments=AttachmentManager(self)
        self.attachments.pack(side='top')
        ttk.Button(self, text='Send', command=self.button).pack(anchor='w')
        self.pack()
        self.mainloop()
    def button(self):
        rcpttos=self.rcpttos.get("1.0",'end-1c').replace(',', ' ').split()
        fromaddr=self.fromaddr.get("1.0",'end-1c')
        fromname=self.fromname.get("1.0",'end-1c')
        subject=self.subject.get("1.0",'end-1c')
        body=self.body.get("1.0",'end-1c')
        attachments=self.attachments.get_attachments()
        self.send(rcpttos, fromaddr, fromname, subject, body, attachments)
    def send(self, rcpttos, fromaddr, fromname, subject, body, attachments):
        mimeapps=[]
        for f in attachments:
            try:
                with open(f, 'rb') as cfile:
                    app=MIMEApplication(cfile.read())
                    app['Content-Disposition']='attachment; filename="%s"' % basename(f)
                    mimeapps.append(app)
            except Exception as error:
                print(error)
        print('Fetched attachments')
        addrlist={}
        for toaddr in rcpttos:
            try:
                server=MXlookup(toaddr.split('@')[1])
                addrlist[server]=addrlist.get(server, [])+[toaddr]
            except IndexError:
                print('Invalid email:', toaddr)
        print('Looked up addresses')
        for server in addrlist:
            toaddrs=addrlist[server]
            msg=MIMEMultipart()
            msg['To']=', '.join(toaddrs)
            msg['From']=email.utils.formataddr((fromname, fromaddr))
            msg['Subject']=subject
            msg.attach(MIMEText(body))
            for app in mimeapps:
                msg.attach(app)
            try:
                smtp=smtplib.SMTP(server)
                print('Connected to', server)
                try:
                    smtp.starttls()
                    print('Started TLS')
                except Exception as error:
                    print(error)
                smtp.send_message(msg)
                print('Sent')
            except Exception as error:
                print(error)
PyMailer()
