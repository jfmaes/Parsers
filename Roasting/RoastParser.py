import argparse
parser = argparse.ArgumentParser(description='Extract hashcat kerberoast hashes from outputs of various tools.')
#parser.add_argument("--tool-name","-t",default="Invoke-Kerberoast",help="The tool of which the output should be parsed")
parser.add_argument("--mode","-m",default="kerberoast",help="the mode to parse: kerberoast or asreproast")
parser.add_argument("--input","-i",required=True,help="the outputfile the tool produced.")
parser.add_argument("--output","-o",help="the full path of where the parsed hashes should be saved.",required=False)
args=parser.parse_args()
OutFile =""
DistinguishedName = ''
Hash = ''
Hashes = []
HashCount = 0
with open(args.input,'r') as file:
    try:
        for line in file:
            if args.mode == "kerberoast":
                if "Hash" in line:
                    Data = line.split(" :")
                    Hash += Data[1].strip()
            if args.mode == "asreproast":
                if "krb5asrep" in line:
                    Hash += line   
            if "                             " in line:
               Hash+= line.strip()
            if line == "\n":
                if Hash:
                    Hash = Hash.lstrip()
                    Hashes.append(Hash)
                    HashCount +=1
                Hash = ""
    except Exception as e:
        print(e)
file.close()
print(str(HashCount) + " Hashes successfully parsed!" +"\n\n\n")
for Hash in Hashes:
    print(Hash)

if args.output:
    output = open(args.output,"w")
    for Hash in Hashes:
        output.write(Hash+"\n")
output.close()

