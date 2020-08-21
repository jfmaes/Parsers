import argparse
parser = argparse.ArgumentParser(description='Extract ntlm and plain text passwords from mimikatz dumps.')
parser.add_argument("--input","-i",required=True,help="the mimikatz dump")
parser.add_argument("--output","-o",help="the full path of where the parsed hashes should be saved.",required=False)
args=parser.parse_args()
Username = ""
Password = ""
NTLM = ""
UniqueUserName = False
UserNamesWritten = []
HashWrittenFor = []
PasswordWrittenFor = []
Record = []
RecordList = []
output = ""
if args.output:
    output = open(args.output,"w")
with open(args.input,'r') as file:
    try:
        for line in file:
            if "Username" in line:
               data = line.split(" :")
               user = data[1].strip()
               if user == "(null)":
                   continue
               Username = user.strip().upper()
               if "UserName:"+Username in Record:
                UserNamesWritten.append(Username)
                Record.append("UserName:"+Username)
                UniqueUserName = True
               else:
                   UniqueUserName = False

            if "NTLM" in line:
                        data = line.split(" :")
                        hash = data[1].strip()
                        NTLM = hash
                        if Username not in HashWrittenFor:
                            Record.append("NTLM:"+NTLM)
                            HashWrittenFor.append(Username)

            if "Password" in line:
                        data = line.split(" :")
                        Password = data[1].strip()
                        if ("(null)" in Password)or (len(Password)> 50) :
                            if Record:
                                RecordList.append(Record)
                                Record = []
                            continue
                        if Username not in PasswordWrittenFor:
                            if UniqueUserName:
                                Record.append("Password:"+Password)
                                RecordList.append(Record)
                            else:
                                for Record in RecordList:
                                    if Username in Record:
                                        Record.append("Password:"+Password)
                            PasswordWrittenFor.append(Username)
                            Record = []
                                
    except Exception as e:
        print(e)
file.close()
for Record in RecordList:
    for item in Record:
        if "UserName" in item:
            print("=========="+item+"==========")
            if output:
                output.write("=========="+item+"==========" + "\n")
        elif "NTLM" in item:
            print(item)
            if output:
                output.write(item+"\n")
        elif "Password" in item:
            print(item)
            if output:
                output.write(item+"\n")
    print("\n")
    if output:
        output.write("\n")
if output:
    output.close()
