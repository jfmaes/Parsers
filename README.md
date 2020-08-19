# Parsers
parsers to make life easier

## mimi parser
Feed the parser your mimikatz logonpassword dump and the parser will give you all the username/ntlm/password combinations without the rest of the lsass junk.
**important** currently the password part of the parsing goes a bit wrong, I will hotpatch it by end of week (23th of August 2020)
NTLM parsing works fine though!

## roast parser
Feed your Invoke-Kerberoast or Rubeus output and the parser will give you a file ready to throw into hashcat.
