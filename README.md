# PyMailer
A Python Mass Mailer
Supports sending emails to many people. Supports use of attachments.

It uses tkinter for the graphics because it is in the python standard library so you don't have to install anything.

It uses email.mime module to allow attachments to be added to the email. It uses tkinter.filedialog to allow native selection of the attachments.

It uses subprocess to the 'host' command on linux or 'nslookup -q=mx' on windows to find the SMTP server for the specified domain. It uses the platform module to determine which command to use and the re module to parse the outputs for the SMTP servers.

The smtplib module is used to actually send to email to the SMTP server.
