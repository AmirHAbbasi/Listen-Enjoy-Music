# Listen & Enjoy © Simple Security & Decoding System
# Mapping Password for security

alphabet = ["@","&"]

alphabet+= [chr(i) for i in range(65,91)]

alphabet+= [chr(i) for i in range(97,123)]

alphabet+= [str(i) for i in range(10)]

def binaryDecode(binary):
    # binary = b'\x11\x00\x10' == X'110010'
    binary=binary.hex()
    res=0
    i=len(binary)-1
    for char in binary:
        if(int(char)):
            res+=2**i
        i-=1
    return res


def fix(binaryStr, size):
    return (size-len(binaryStr))*"0"+binaryStr

def Bin2Num(binStr):
    i=len(binStr)-1
    res=0
    for char in binStr:
        if(int(char)):
            res+=2**i
        i-=1
    return res

# For maximum 64 states (6 Bits)
def encode(index):
    global alphabet
    return alphabet[index]

def decode(char):
    global alphabet
    return alphabet.index(char)
    
def date_encode(birthday):  # "1998-07-23" --> char(2)
    date = birthday.split("-")
    year = bin(int(date[0])-1920)[2:]
    year = fix(year, 7)



    month = bin(int(date[1]))[2:]
    month = fix(month, 4)


    day = bin(int(date[2]))[2:]
    day = fix(day, 5)


    string = year+month+day
    


    return string


def date_decode(byte):
    string = byte.hex()
    
    y,m,d = string[:7], string[7:11], string[11:]

    y = Bin2Num(y)
    m = Bin2Num(m)
    d = Bin2Num(d)


    return 1920+y,m,d



"""    

def Char2Bin(char,uchar):
    return bin(ord(char)+ord(uchar))[2:]




def passMap(uname, password):  # Password -->  StoredPassword
    u=len(uname)
    if(ord(uname[0])%3):
        password =password[-1:0:-1]+password[0]
    P=""
    for i in range(len(password)):
        P+=Char2Bin(password[i],uname[i%u])
    #P=
    return Bin2Num(P)
"""

def passMap(uname, password):  # Password -->  StoredPassword
    counter=0
    for i in password[:len(password)//2]:
        counter+=ord(i)+ord(uname[0])
    res=alphabet[counter%64]
    for i in password[len(password)//2:]:
        counter+=ord(i)+ord(uname[-1])
    res+=alphabet[counter%64]
    return res


















    

        

