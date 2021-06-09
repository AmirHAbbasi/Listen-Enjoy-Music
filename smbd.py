 

"""
Table Users-------------------------
uid int PK            
string username
string password
string image_id # by default : 00 which means 00.jpg (null image)
int money
3 BITS Type     # 0 : user, 1 : premium user, 2 : artist, 3 : valid_artist   
string email
2 Byte birthday



Table AlbumArtist-------------------------
id artist FK     # musics made by an artist  (an album can be made by multi artist) 
id album FK          



Table Follow-------------------------
id followed_user                
id follower_username             


Table Music-------------------------
int id PK
string name
int Minutes  # length
int Seconds
4 BYTE Genre                       
int album FK
4 BYTE Format # 0 : MPEG, 1:WAV ,...   
int listened  # how many users listened this
string image_id # by default : 00 which means 00.jpg (null image)
int(7BIT) rate        # music rate (0-100 likes)
int likes
int dislikes
Date date_created
lyric_id int FK  

Table Events--------------------------
Date event_date 3BYTES       # 7bits(year from 2020) 4bits(months 1-12) 5bits(day 1-30) 5bits(hour 1-24) 
Date event_minutes 1BYTE     # 6 bits (1-60) 
id host_user                 


Table Share-------------------------
id sharerReceiver_user FK   
id shareSender_user FK      
int(2BITS) Type # Type of Shared obj 01 : Music, 10 : PlayList, 11 : Album, 00 : Event 
int obj_id  FK 


Table Album-------------------------
int id PK                  
1 BIT is_playList  
string name
id creator_uname FK    
Date date_created             # 7bits(year from 2020) 4bits(months 1-12) 5bits(day 1-30)  


Table AlbumMusicList----------------
int album_id FK
int music_id FK

Table Lyric------------
id int PK          
creator int FK # creator user_id 
char(1000)      

Table Comments--------------------
mid int FK # Music Id
commenter int FK 
Date submitted     
content char(120) 


"""





import sqlite3
import random, datetime
import ytiruces


interface=[]  

#table users already exists




class DB:
    def __init__(self,db_name="art"):
        self.name = db_name
        if(db_name[-3:]!=".db"):
            self.name+=".db"
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
        self.log = open("logs/{}.txt".format(datetime.date.today()), "a")
        self.log.write("\n####################################################REFERESH####################################################\n")
        self.log.flush()
    def add_Table(self,table_name,attrs, ReMakeIfExist=False):
        # attrs = "attr0 type0 [exp0], attr1 type1 [exp1], ..."   example : "FIRST_NAME CHAR(20) NOT NULL, LAST_NAME CHAR(20),..."
        
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        cmd = "CREATE TABLE "+table_name+"("+attrs+")"
        try:
            self.cursor.execute(cmd)
            self.log.write(cmd)
        except Exception as e:
            if("already exists" in str(e)):
                if(ReMakeIfExist):
                    self.cursor.execute("DROP TABLE "+table_name)
                    self.cursor.execute(cmd)
                    self.log.write(cmd)
            else:
                raise(e)
        
        self.conn.commit()
        self.log.write("\n-----------------")
        self.log.flush()
    def insert_records(self,table_name,attrs=""):
        # for example interface[0] = (9,"NUM")
        global interface
        # attrs = "attr0, attr1, ..."
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        cmd="INSERT INTO "+table_name+"("+attrs+") VALUES "
        cmd=cmd.replace("()"," ")
        for record in interface:
            cmd+=str(record)+","
        if(cmd[-1]==","):
            cmd=cmd[:-1]
        
        self.log.write(cmd)
        self.cursor.execute(cmd)  
        interface=[]
        self.conn.commit()
        self.log.write("\n-----------------")
        self.log.flush()
    def searchSubString(self, searched_attr, substring, table_name,condition="",attrs="*"): #"SELECT * from EMPLOYEE WHERE AGE <23"
        global interface
        # SELECT * FROM table WHERE attr  LIKE '%[substring]%';
        # condition = "AGE <23"
        # attrs = "attr0, attr1, ..."
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        cmd = "SELECT "+attrs+" FROM "+table_name
        cmd+=" WHERE {0} LIKE '%{1}%'".format(searched_attr, substring)
        if(condition):
            cmd+=" AND "+condition
        self.log.write(cmd)
        self.cursor.execute(cmd)
        interface=cursor.fetchall()   
        self.log.write("\n-----------------")
        self.log.flush()
    def record_search(self,table_name,condition="",attrs="*"): #"SELECT * from EMPLOYEE WHERE AGE <23"
        global interface
        # condition = "AGE <23"
        # attrs = "attr0, attr1, ..."
        cmd = "SELECT "+attrs+" FROM "+table_name
        if(condition):
            cmd+=" WHERE "+condition
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        self.log.write(cmd)
        self.cursor.execute(cmd)
        interface=self.cursor.fetchall()
        self.log.write("\n-----------------")
        self.log.flush()
    def delete(self,table_name,condition): # "DELETE from COMPANY where ID = 2;"
        # condition = "ID = 2"
        cmd = "DELETE from "+table_name+" WHERE "+condition+";"
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        self.log.write(cmd)
        self.cursor.execute(cmd)
        self.conn.commit()
        self.log.write("\n-----------------")
        self.log.flush()
    def update(self,table_name): # "UPDATE COMPANY set SALARY = 25000.00 where ID = 1"
        # for example interface[0] = (command,condition)
        # command = "SALARY = 25000.00"
        # condition = "ID = 2"   
        global interface
        cmd = "UPDATE "+table_name+" SET {0} WHERE {1}"
        self.log.write("\n--------{}---------\n".format(datetime.datetime.now()))
        for rec in interface:
            self.cursor.execute(cmd.format(rec[0],rec[1]))
            self.log.write(cmd.format(rec[0],rec[1]))
        interface=[]
        self.conn.commit()
        self.log.write("\n-----------------")
        self.log.flush()
    def getCountEntities(self,table_name):
        cmd = "SELECT seq from sqlite_sequence WHERE name='{}'".format(table_name)
        self.cursor.execute(cmd)
        count = self.cursor.fetchall()
        if(count):
            count = count[0][0]  # [(9,)]
        else:
            count = 0
        return count
    def connect(self):
        self.conn = sqlite3.connect(self.name)
        self.cursor = self.conn.cursor()
    def close(self):
        self.conn.close()

        
db = DB("art")


# Create Tables 



#db.add_Table("Users","uid INTEGER PRIMARY KEY AUTOINCREMENT, uname char(25), password int, image_id char(10) DEFAULT '00', money int DEFAULT 0, type char(1), email char(30), birthday char(4)")

db.add_Table("Users","uid INTEGER PRIMARY KEY AUTOINCREMENT, name char(25), lname char(25) , uname char(25), password char(2), money int DEFAULT 0, type b(2) DEFAULT X'00', email char(30), birthday b(16)")





db.add_Table("AlbumArtist","artist int, album int")

db.add_Table("Follow","followed_user int, follower_username int")

db.add_Table("Music","""id INTEGER PRIMARY KEY AUTOINCREMENT, name char(25),
album int,Minutes int,Seconds int, format char(1), listened int DEFAULT 0, rate b(7) DEFAULT X'110010', likes int DEFAULT 0, dislikes int DEFAULT 0 , lyric_creator int
             """)

db.add_Table("Events","event_date char(6), event_minutes char(1), host_user int")

db.add_Table("Share","sharerReceiver_user int, shareSender_user int, type char(1), obj_id int")

db.add_Table("Album","id INTEGER PRIMARY KEY AUTOINCREMENT, is_playList char(1), name char(25), creator_uname int, date_created b(16), genre b(4) DEFAULT X'0000'")



db.add_Table("Lyric","lid INTEGER PRIMARY KEY AUTOINCREMENT, creator int")
db.add_Table("Comments","mid int, commenter int, date_submitted char(10), content char(120), FOREIGN KEY (commenter) REFERENCES Users(uid)")




db.add_Table("ActiveUsers","""user_id int, active_id nvarchar(11), active_time date DEFAULT CURRENT_TIMESTAMP,
                              FOREIGN KEY (user_id) REFERENCES Users(uid) ON DELETE CASCADE""")



"""
interface=[("a",54)]
db.insert_records("Users","uname,password")
"""


# Functions

# add command  "global interface" at first of all these functions ...........


def generatePass():
    res = ""
    while(len(res)<7):
        res=str(random.random())[2:10]
    return res

def activateUser(uid):
    global interface
    
    db.delete("ActiveUsers","user_id={}".format(uid))
        
    # insert user to actives
    d = datetime.date.today()
    _id = str()+str(generatePass())
    interface = [(uid, _id)]
    db.insert_records("ActiveUsers", "user_id, active_id")
        
    return _id   

    
def getUserId(active_id):
    global interface
    db.record_search("ActiveUsers",condition="active_id={} AND julianday('now') - julianday(active_time) < 7".format(active_id))
    if interface:
        return interface[0][0]
    else:
        return None

def logout(active_id):
    db.delete("ActiveUsers","active_id={}".format(active_id))
    
    


    
def searchSubstr(substr, table="Music", condition="", attrs="*"):
    nameAttr={ "Music":"name",
               "Users":"uname",
               "Album":"name"
        }
    global interface
    db.searchSubString(searched_attr=nameAttr[table], substring=substr, table_name=table, condition=condition,attrs=attrs)
    return interface


def check_uname(uname):
    global interface
    db.record_search("Users",condition="uname='"+uname+"'")
    return bool(interface)
        
    
def new_user(fname,lname,uname,passwrd,email,birthday,_type="user"):
    global interface
    # _type = "user", "premium", "artist", "valid_artist"
    if(check_uname(uname)):
        return 1
    atrs = "name ,lname , uname , password , email"

    global interface
    
    interface=[(fname,lname,uname,ytiruces.passMap(uname, passwrd),email)]
    
    db.insert_records("Users",atrs)
    
    interface=[("birthday=X'{}'".format(ytiruces.date_encode(birthday)),"uname='{}'".format(uname))]
    
    if(_type!="user"):
        interface.append(("type=X'01'","uname='{}'".format(uname)))
    
    db.update("Users")
    
    return 0




def get_user_info(uname, pwd="a", allow=False):
    global interface
    if(not allow):
        if(type(pwd)==type("")):
            pwd=ytiruces.passMap(uname, pwd)
        db.record_search("Users",condition="uname='"+uname+"' AND password='{}'".format(str(pwd)))
    else:
        db.record_search("Users",condition="uid="+str(uname))
    if(not interface):
        return 0
    result={"id":interface[0][0],
            "name":interface[0][1],
            "lname":interface[0][2] ,
            "uname":interface[0][3] ,
            "money":interface[0][5],
            "type":type_decode(interface[0][6]),
            "birthday":ytiruces.date_decode(interface[0][-1])}        
    return result



def type_decode(binary): ###########################
    T = {b'\x00' : "User",
        b'\x01' : "Not Verified Artist"
        }
    return T[binary]

def genre_decode(binary): ###################################
    G = { b'\x00\x00' : "Pop"
        }
    return G[binary]

def format_decode(binary): ########################
    print(binary)
    G = { b'\x00\x00' : "MPEG"
        }
    try:
        return G[binary]
    except KeyError:
        return "MPEG"


def get_Album_info(aid):
    global interface
    db.record_search("Album",condition="id={}".format(str(aid)))
    return {"playList": interface[0][1],
            "name":interface[0][2],
            "creator":interface[0][3],
            "date":ytiruces.date_decode(interface[0][4]),
            "genre":genre_decode(interface[0][5])
        }




        
def get_music_comments(music_id):
    global interface
    db.record_search("Users, Comments",condition="Comments.mid={} AND Comments.commenter=Users.uid".format(str(music_id)),attrs="Users.uid, Users.name, Users.lname, Comments.date_submitted, Comments.content")
    res=[]
    for elm in interface:
        res.append([elm[0], elm[1], elm[2], elm[3], elm[4]])
    return res

def get_user_albums(uid):
    global interface
    db.record_search("Album",condition="creator_uname={}".format(str(uid)))
    res=[]
    for elem in interface:
        res.append([elem[0], elem[1], elem[2], elem[3], ytiruces.date_decode(elem[4]), genre_decode(interface[0][-1])])
    return res
def get_album_musics(album_id):
    global interface
    db.record_search("Music",condition="album={}".format(album_id))
    for i in range(len(interface)):
        interface[i]=[interface[i][0],
                      interface[i][1],
                      interface[i][3],
                      interface[i][4],
                      format_decode(interface[i][5]),
                      interface[i][6],
                      ytiruces.binaryDecode(interface[i][7]),
                      interface[i][8],
                      interface[i][9],
                      interface[i][10]]
    return interface # [ [id , name, minutes, seconds, format, listened, rate b(7) DEFAULT X'110010', likes, dislikes, lyric_creator int] ,...]



    
def delete_user(uid):
    global interface
    uid=str(uid)
    # delete from users where username=uname
    db.delete("Users","uid='{}'".format(uid))
    
    # set artist=NULL from AlbumArtist where artist = uname
    interface = [("artist=NULL","artist={}".format(uid))]
    db.update("AlbumArtist")

    #delete from Follow where followed_user = uname or follower_username = uname
    db.delete("Follow","followed_user={0} or follower_username={0}".format(uid))

    #delete from Events where host_user = uname
    db.delete("Events","host_user ={}".format(uid))

    #delete from Share where sharerReceiver_user = uname or shareSender_user=uname
    db.delete("Share","sharerReceiver_user={0} or shareSender_user={0}".format(uid))

    #set creator_uname=NULL from Album where creator_uname=uname
    interface = [("creator_uname=NULL","creator_uname={}".format(uid))]
    db.update("Album")    

    # delete his comments
    db.delete("Comments","commenter={}".format(uid))
    
    return 0  # No Error




def delete_shared_contents(uid):
    # Deletes All Shared objs shared to user
    db.delete("Share","sharerReceiver_user='{}'".format(uid))

def setLyric(music_id, lyricText, creator_user_id):
    global interface
    #### Music.lyric_creator = creator_user_id
    ### save .txt file as [music_id].txt

def get_money(uid):
    global interface
    db.record_search("Users",condition="uid={}".format(uid),attrs="money")
    if(interface):
        return interface[0][0]
    return 0

def change_money(uid, cost):
    m = get_money(uid)+cost
    if(m>-1):
        interface = [("money={}".format(m),"uid={}".format(uid))]
        db.update("Users")
        return 0
    return 1  # Error (No Enough Money !)





def mailto(email, new_pd): #????????????????????????????????????????
    with open("ForgetPass.txt", "a") as file:
        file.write(email+" Password:"+new_pd)
    file.close()

def forget(email, birthday):
    global interface
    db.record_search("Users",condition="email='{0}' AND birthday=X'{1}'".format(email, ytiruces.date_encode(birthday)),attrs="uid,uname")

    if(not interface):
        return 0
    new_pd = generatePass()

    p = ytiruces.passMap(interface[0][1], new_pd)

    interface = [("password='{}'".format(p), "uid={}".format(interface[0][0]))]

    db.update("Users")
    mailto(email, new_pd)
    return 1

def getMusicsByGenre(genreID):
    pass ############################




############################
def auto_mail(email, new_pd, sender="info@listenj.oy", password="1234"):
    server=email.split("@")[1]
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    message = MIMEMultipart()

    body = """
        <h1>ListenJoy!</h1>
        <p>User! your new password is:{}</p>
        """.format(new_pd)
    
    message['From'] = sender 
    message['To'] = email  
    message['Subject'] = "Forget Password" 
    message.attach(MIMEText(body, 'plain'))
    
    server="smtp.gmail.com: 587"
    print(server)
    server = smtplib.SMTP(server)
    try:
        print("startTls")
        server.starttls(keyfile=None, certfile=None, context=None)
        print("TLS Successed!")
    except smtplib.SMTPNotSupportedError:
        pass
    print("2")
    print(server.ehlo(sender.split("@")[1]))
    print(server.helo(sender.split("@")[1]))
    #server.login(sender, password, initial_response_ok=True)

    """
    server.auth_plain() smtplib.SMTPSenderRefused:
    (530, b'5.7.0 Authentication Required. Learn more at\n5.7.0  https://support.google.com/mail/?p=WantAuthError a6sm214526ejv.4 - gsmtp', 'info@listenj.oy')
    """
    
    print("Authed!")
    server.sendmail(sender, email, message.as_string())
    print("3")
    server.quit()
############################
    
#auto_mail(email="william.vilhalm.johnson.official@gmail.com", new_pd="1234")
#auto_mail(email="abbasi_amir@comp.iust.ac.ir", new_pd="1234")


'''
email="am.abb.2018@gmail.com"

auto_mail(email, "1234")
print(message)
'''





# initialize
"""
Users:
0 Abbasi_Admin    ytiruces.passMap(Abbasi_Admin, adm4321in)   00   1000   user  admin@   ytiruces.date_encode(2000-01-01)
1 Nasser_Abdollahi    ytiruces.passMap(Nasser_Abdollahi, nasser1234)    123   0   artist  nasser@   ytiruces.date_encode(1983-07-22)
2 Garsha_Rezaee    ytiruces.passMap(Garsha_Rezaee, garshaa345)    00   0   artist  garsha@   ytiruces.date_encode(1987-08-02)

Album:
0 0  Naseria  [Nasser_Abdollahi]  2003.04.25
1 0  Hypnothism  [Garsha_Rezaee]  2020.02.13

AlbumArtist:
1  0
2  1



Music:
0 Tanha 0 0 0 0 01  0  10 5 2003.5.8 NULL
1 Khooneh 0 0 0 0 01  0 12 9 2003.5.8 0
2 Fatemeh 0 0 0 0 01  0 13 2 2003.5.8 NULL
3 Hypnotism 1 0 0 00  0 15 0 2003.5.8 NULL


Comments:
0 0 2003.5.8 خيلي عاليه! پيشنهاد ميکنم به شما هم
0 1 2003.12.28 Great Music!
1 1 2012.6.5 Ashghaleeeeeeeee!! Goosh Nadin!!



"""


def init_db():
    global interface

    # Users & Artists
    attrs="uid, name, lname, uname,password, email"
    interface=[(0,"Adm","in","Abbasi_Admin", ytiruces.passMap("Abbasi_Admin", "adm4321in"),"admin@"),
              (1,"Nasser","Abdollahi","Nasser_Abdollahi",ytiruces.passMap("Nasser_Abdollahi", "nasser1234"),"nasser@"),
              (2,"گرشا","رضايي","Garsha_Rezaee",ytiruces.passMap("Garsha_Rezaee", "garshaa34"),"garsha@"),
              (3,"عليرضا","افتخاري","Alireza_EFT",ytiruces.passMap("Alireza_EFT", "Eftekhar4321"),"EftKhar@gmail.com"),
              (4,"Hayedeh","","Hayedeh",ytiruces.passMap("Hayedeh", "h1234ay"),"Hayedeh@gmail.com")
              ]
    
    db.insert_records("Users",attrs)

    # Set Users Birthday
    interface=[("birthday=X'{}'".format(ytiruces.date_encode("1983-07-22")),"uid=1"),
               ("type=X'01'","uid=1"),
               ("type=X'01'","uid=2"),("type=X'01'","uid=3"),("type=X'01'","uid=4"),
               ("birthday=X'{}'".format(ytiruces.date_encode("1987-08-02")),"uid=2"),
               ("birthday=X'{}'".format(ytiruces.date_encode("1998-11-23")),"uid=0"),
               ("birthday=X'{}'".format(ytiruces.date_encode("1958-3-30")),"uid=3"),
               ("birthday=X'{}'".format(ytiruces.date_encode("1942-5-10")),"uid=4")]
    db.update("Users")


    # Albums
    interface=[(0,0,"ناصريا",1), (1,0,"HYPNOTISM",2), (2,0,"چلچله",3), (3,0,"Sea",2), (4,0,"بهترين هاي کلاسيک",4), (5,0,"صياد",3), (6,0,"شب تار جدايي",3)  
               ]
    attrs = "id, is_playList, name, creator_uname"
    db.insert_records("Album",attrs)


    # Set Albums Date
    interface=[("date_created=X'{}'".format(ytiruces.date_encode("2003-04-25")),"id=0"),
               ("date_created=X'{}'".format(ytiruces.date_encode("2020-02-13")),"id=1"),
               ("date_created=X'{}'".format(ytiruces.date_encode("2010-07-23")),"id=2"),
               ("date_created=X'{}'".format(ytiruces.date_encode("2019-11-01")),"id=3"),
               ("date_created=X'{}'".format(ytiruces.date_encode("1982-6-27")),"id=4"),
               ("date_created=X'{}'".format(ytiruces.date_encode("2004-11-7")),"id=5"),
               ("date_created=X'{}'".format(ytiruces.date_encode("1992-1-2")),"id=6")]
    db.update("Album")


    # Musics
    attrs = "id, name, album,Minutes,Seconds, lyric_creator"
    interface=[(0,"Tanha",0,4,14,1), 
            (1,"Khooneh",0,4,19,1),
            (2, "Fatemeh",0,4,28,1),
            (3,"Hypnotism", 1,2,38, 2),
             (4,"چلچله", 2,6,46, "NULL"),
            (5,"گلهاي اطلسي", 2,5,43, "NULL"),
               (6,"اي نامت از دل و جان", 2,6,43, "NULL"),
               (7,"يارايارا", 5,7,43, "NULL"),
               (8,"صياد", 5,4,10, "NULL"),
               (9,"نسيم آشنايي", 6,4,11, "NULL"),
               (10,"يا مولا دلم تنگ آمده", 6,5,26, "NULL"),
               (11,"شاخ شمشاد", 6,4,54, "NULL"),
               (12,"Ey Mah!", 6,5,45, 0),
               (13,"Darya Nemiram", 3,3,18, "NULL"),
               (14,"Darya Darya!", 3,2,48, "NULL"),
               (15,"گل واژه", 4,3,50, "NULL"),
               (16,"زندگي سلام", 4,7,10, "NULL"),
               (17,"سيه چشمون", 4,6,20, "NULL"),
               (18,"دل را ببين", 2,6,44, "NULL")
               ]
    db.insert_records("Music",attrs)

    #Comments
    interface=[(0,0,"خيلي عاليه! پيشنهاد ميکنم به شما هم","2003.5.8"),
                (0,1,"Great Music!","2003.12.28"),
                (1,1,"Ashghaleeeeeeeee!! Goosh Nadin!!","2012.6.5"),
               (5,0,"عاشق سنتي هستم. عليرضا افتخاري عالي ميخونه!","2020.5.21"),
               (5,1,"Great!","2013.1.1")
                ]
    db.insert_records("Comments","mid, commenter,content,date_submitted")




#init_db()

    





