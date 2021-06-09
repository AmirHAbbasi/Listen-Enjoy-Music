from flask import Flask, render_template, request, redirect, send_file, jsonify
import smbd

import os 
cp = os.path.dirname(os.path.realpath(__file__))+"/"

Project_name='Le-Music-Player'
app=Flask(Project_name,template_folder='templates', static_url_path = "/elements" , static_folder = "elements")



def invalid(String): ###############
    # valid ranges : [33,...,122]
    for i in String:
        if not(ord(i) in range(33,123)):
            return True
    return False



# Home Page

@app.route('/',methods=['GET']) #decorator
def index():
    return render_template('login.html', message="")


# content
@app.route('/cdn/<path:file>')
def custom_static(file):
    try:
        return send_file("static/SourceFiles/"+file)
    except FileNotFoundError:
        return ('', 204)


# Login Page

@app.route('/enter',methods=['GET']) #decorator
def enter():
    return render_template('login.html', message="")


# Check Email,birth parity of Forget Pass Request
@app.route("/exists", methods=["GET"])
def exists():
    em = request.args.get("em")
    bd = request.args.get("bd")
    smbd.db.connect()
    if(not smbd.forget(em,bd)):
        smbd.db.close()
        return "F"
    smbd.db.close()
    return "T"


# getMusicsByGenre
@app.route('/genre=<genre>',methods=['GET']) 
def genre(genre):  ###############################################
    return render_template('login.html', message="")



# User Profile
@app.route('/uprof<iid>',methods=['GET']) #decorator
def user(iid):
    smbd.db.connect()
    info=smbd.get_user_info(iid, allow=True)
    if(not info):
        smbd.db.close()
        return render_template("NotFound.html")
    alb = smbd.get_user_albums(iid)
    smbd.db.close()
    return render_template('UserProfile.html', user_info=info, albums=alb, comments=[], iid=iid)

# Album Profile
@app.route('/album<iid>',methods=['GET']) #decorator
def album(iid):
    smbd.db.connect()
    try:
        info=smbd.get_Album_info(iid)
    except IndexError:
        smbd.db.close()
        return render_template("NotFound.html")
    cr = smbd.get_user_info(info["creator"], pwd="a", allow=True)
    mu = smbd.get_album_musics(iid)
    smbd.db.close()
    return render_template('AlbumProfile.html', album_info=info, musics=mu, iid=iid, creator=cr)




# Hidden Backend Username Check
@app.route("/check", methods=["GET"])
def check():
    username = request.args.get("q")
    if(invalid(username)):
        return "V"
    smbd.db.connect()
    if(smbd.check_uname(username)):
        smbd.db.close()
        return "T"
    smbd.db.close()
    return "F"

# Hidden Backend Comment Provider
@app.route("/comments", methods=["GET"])
def comments():
    mid = request.args.get("q")
    smbd.db.connect()
    a = smbd.get_music_comments(mid)
    smbd.db.close()
    return jsonify(a) # [[0, '2003.5.8', 'خيلي عاليه! پيشنهاد ميکنم به شما هم'], [1, '2003.12.28', 'Great Music!']]

# Hidden Backend Lyric Provider
@app.route("/lyric", methods=["GET"])
def lyric():
    mid = request.args.get("q")
    try:
        return jsonify(open("static/SourceFiles/Lyrics/{}.txt".format(mid), "r").read())  
    except FileNotFoundError:
        return ('', 404)

# Hidden Backend Lyric Added
@app.route("/addlyric", methods=["GET","POST"])
def addlyric():
    mid=""
    lyric=request.get_data()
    for i in lyric:
        if(i==45):
            break
        mid+=chr(i)
    mid=mid.split(",")
    uid=int(mid[0])
    mid=mid[1]
    f=open("static/SourceFiles/Lyrics/{}.txt".format(mid),"wb") #????????????
    f.write(lyric)
    f.close()
    #smbd.lyricAdded(mid, uid) ##########
    return ('', 204)
    

# Register Page

@app.route('/reg',methods=['GET'])
def reg():
    return render_template('register.html')


# Submit new user (Redirector)

@app.route('/newser',methods=['GET', 'POST'])
def newser():
    fname= request.args.get("firstName") 
    lname= request.args.get("LName") 
    _type = request.args.get("t")
    uname = request.args.get("u")
    pas = request.args.get("p")
    mail = request.args.get("m")
    y = request.args.get("year")
    m = request.args.get("month")
    d = request.args.get("day")
    date = "{0}-{1}-{2}".format(y,m,d)

    _type = "user" if _type=="true" else "artist"

    smbd.db.connect()
    
    user = smbd.new_user(fname,lname,uname,pas,mail,date,_type)  # BIRTH ??????????

    smbd.db.close()
    return render_template('login.html', message="Welcome! Now Login To your new account!")


# Get Profile Page for a user

@app.route('/login',methods=['GET', 'POST'])  
def login():
    smbd.db.connect()
    data=request.form
    u_info = smbd.get_user_info(data["uname"],data["ps"])
    if(u_info):
        alb = smbd.get_user_albums(u_info["id"])
        actid = smbd.activateUser(u_info["id"])
        smbd.db.close()
        return render_template('UserProfile.html',
                        user_info=u_info,
                        albums=alb,
                        comments=[],
                        iid=u_info["id"],
                        active_id = actid)
    smbd.db.close()
    return render_template('login.html', message="Username or Password is incorrect !")

@app.route('/logout',methods=['GET', 'POST'])  
def logout():
    smbd.db.connect()
    smbd.logout(request.form["activeid"])
    smbd.db.close()
    return render_template(login.html)
    

@app.errorhandler(404)
def page_not_found(e):
    return render_template('NotFound.html'), 404

 
app.run(port=8080)














