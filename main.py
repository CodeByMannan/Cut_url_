from flask import Flask  , redirect , render_template  , request
import sqlite3
import string
import random 

app = Flask (__name__)
# some important functions................
def db_create():
    con = sqlite3.connect("urls.db")
    cursor = con.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS urls (
                   title TEXT NOT NULL,
                   longs TEXT NOT NULL,
                   shorts TEXT PRIMARY KEY
                   )

''')
    con.commit()
    return con

def r_generator(len = 5):
    chrs = string.ascii_letters + string.digits
    r = "".join(random.choice(chrs) for _ in range (len))
    return r

def url_exists(short):
    con = sqlite3.connect("urls.db")
    cursor = con.cursor()
    cursor.execute("SELECT 1 FROM  urls WHERE shorts = ?", (short,))
    exist = cursor.fetchall()
    con.close()
    return exist

def add_url(title , long_url, short):
    con = sqlite3.connect("urls.db")
    cursor = con.cursor()
    cursor.execute("INSERT INTO urls (title , longs , shorts) VALUES (? , ? ,? )",
                   (title ,long_url , short ))
    con.commit()
    con.close()


def list_all():
    con = sqlite3.connect("urls.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM urls")
    date = cursor.fetchall()
    con.commit()
    con.close()
    return date

#some variables..........
err = None
# routs............
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/short",methods = ['POST'])
def short():
    long_url = request.form.get("long_url")
    custom = request.form.get("custom_url")
    title = request.form.get("title")

    short = custom if custom else r_generator()

    if url_exists(short):
        err = f"{short} allready exists"
        return render_template("short.html" , error = err)
    try:
        add_url(title , long_url , short)
        short_url = f"{request.host_url}{short}"
        return render_template("short.html" , sh = short_url,
                               org = long_url, 
                                t = title )
    except Exception as e:
        print(f"eeeeeeeeeeeeeeeeeeeeeeeeerrrrrrrrrrrrrrrrooooooooooooorrrrrrrrrr +========={e}")
    return render_template("short.html")




@app.route("/<short>")
def get_all(short):
     if short == "list":
         all_date = list_all()
         return render_template("list.html" , date  =all_date)
     con = sqlite3.connect("urls.db")
     cursor = con.cursor()
     cursor.execute("SELECT longs FROM urls  WHERE shorts = ? ", (short,))
     result = cursor.fetchone()
     con.commit()
     con.close()

     if result:
         return redirect(result[0])
     else:
         return "error is here"


app.route("/list")
def go_to():
    return render_template("list.html")

    


if __name__ =="__main__":
    db_create()
    app.run(debug=True)