from couchdb import Server
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Regexp






class LoginForm(FlaskForm):
    username = StringField("username")
    password = PasswordField("password")


class PCAP2Form(FlaskForm):
    VALID_RESP = "Nope, Try Again"
    EVENT_ID = "PCAP2"
    Q1_VALIDATOR = Regexp("ysbinstall_1000489_3.exe", message=VALID_RESP)
    PCAP2_1 = StringField(label="What is the name of the malicious executable?", validators=[Q1_VALIDATOR],
                          id="PCAP2_1")

    Q2_VALIDATOR = Regexp("216.127.33.119", message=VALID_RESP)
    PCAP2_2 = StringField(label="What is the source IP address of the malicious download?", validators=[Q2_VALIDATOR],
                          id="PCAP2_2")

    Q3_VALIDATOR = Regexp("69.64.34.124", message=VALID_RESP)
    PCAP2_3 = StringField(label="What is the IP address of the IRC server?", validators=[Q3_VALIDATOR], id="PCAP2_3")

    Q4_VALIDATOR = Regexp("Recursion desired: Do query recursively", message=VALID_RESP)
    PCAP2_4 = StringField(label="For the DNS query,  which flag is set for the hostname www.ysbweb.com?",
                          validators=[Q4_VALIDATOR], id="PCAP2_4")


class PCAP1Form(FlaskForm):
    VALID_RESP = "Nope, Try Again"
    EVENT_ID = "PCAP1"

    Q1_VALIDATOR = Regexp("FTP", message=VALID_RESP)
    PCAP1_1 = StringField(label="What protocol is being used to connect to the destination?", validators=[Q1_VALIDATOR],
                          id="PCAP1_1")

    Q2_VALIDATOR = Regexp("creditus.com", message=VALID_RESP)
    PCAP1_2 = StringField(label="What is the URL the attacker trying to gain access to?", validators=[Q2_VALIDATOR],
                          id="PCAP1_2")

    Q3_VALIDATOR = Regexp("Fred", message=VALID_RESP)
    PCAP1_3 = StringField(label="What username is the attacker attempting to use?", validators=[Q3_VALIDATOR],
                          id="PCAP1_3")

    Q4_VALIDATOR = Regexp("bruteforce", message=VALID_RESP)
    PCAP1_4 = StringField(label="What type of attack is the user attempt to execute?", validators=[Q4_VALIDATOR],
                          id="PCAP1_4")
