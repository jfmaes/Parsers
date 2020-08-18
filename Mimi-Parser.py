import argparse
parser = argparse.ArgumentParser(description='Extract ntlm and plain text passwords from mimikatz dumps.')
parser.add_argument("--input","-i",required=True,help="the mimikatz dump")
parser.add_argument("--output","-o",help="the full path of where the parsed hashes should be saved.",required=False)
args=parser.parse_args()
Username = ""
Password = ""
NTLM = ""
UniqueUserName = False
EndOfRecord = False
UserNames = []
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
               if Username not in UserNames:
                print("====="+Username+"=====")
                UserNames.append(Username)
                if output:
                    output.write("====="+Username+"=====" + "\n")
                UniqueUserName = True
            if "NTLM" in line and UniqueUserName:
                        data = line.split(" :")
                        hash = data[1].strip()
                        NTLM = hash
                        print("NTLM: " + NTLM)
                        if output:
                            output.write("NTLM: " + NTLM + "\n")
            if "Password" in line:
                        data = line.split(" :")
                        Password = data[1].strip()
                        if ("(null)" in Password)or (len(Password)> 50) :
                            UniqueUserName = False
                        else:
                            print("Password: " + Password)
                            if output:
                                output.write("Password: " + Password +"\n")
                        UniqueUserName = False
    except Exception as e:
        print(e)
file.close()
if output:
    output.close()
