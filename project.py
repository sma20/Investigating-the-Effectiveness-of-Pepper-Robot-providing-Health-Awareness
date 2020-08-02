from flask import Flask, render_template, redirect, url_for, json, request, make_response, session
from user import insertUser, getUser, addFood,getFood
import requests
import urllib.parse
import os
import shutil
from flask import Response, send_file, redirect, url_for
from camera import Camera
import numpy as np
import face_recognition
import time
import socket
from datetime import datetime
from flask_socketio import SocketIO
import pyttsx3
from threading import Thread
import mac_say

from fatsecret import Fatsecret


# Threading Class
class Threader(Thread):
    def __init__(self, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

    def run(self):

        tts_engine = pyttsx3.init()
        tts_engine.say(self._args)
        tts_engine.runAndWait()



fs = Fatsecret('7093457f3a1d4177a4dfb16274b4b558', '331e4a40e22a446da7cb3aa27ea2a3ad')

camera = None

url = 'http://www.fruityvice.com/api/fruit/all'
url1 = 'https://api.nutridigm.com/api/v1/nutridigm/healthconditions?subscriptionId=123'
#url = 'http://api.nutridigm.com/api/v1/nutridigm/fooditems?subscriptionId=all'
#url = 'http://api.foodpairing.com/ingredients/4243'
#url = 'https://nutritionix-api.p.rapidapi.com/v1_1/search/96b8975b0fmshbe602fc89becfd4p1ebb78jsn9a364f5aec09'
url_goodfor='https://api.nutridigm.com/api/v1/nutridigm/goodfor?subscriptionId=123&itemID=280&problemId=2'
url_topitemstoconsume='https://api.nutridigm.com/api/v1/nutridigm/topitemstoconsume?subscriptionId=123&problemId=2'
url_thingstoavoid='https://api.nutridigm.com/api/v1/nutridigm/topitemstoavoid?subscriptionId=123&problemId=2'
url_suggest='https://api.nutridigm.com/api/v1/nutridigm/suggest?subscriptionId=123&problemId=2&fg2=d'
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['itemID'], todo_item['fiText']))



problem_list = [[0, 'None'],[ 15,"Rheumatoid Arthritis"], [ 64,"Osteoarthritis"], [ 25,"Osteoporosis"], [ 30,"Diabetes Type-1"], [16,"Diabetes Type-2"], [ 20,"Cancer Risk"], [ 2,"High Blood Pressure"], [ 1,"High Cholesterol"], [ 196,"joint pain"], [ 197,"Kidney stones (Uric)"], [ 224,"Muscle aches/pains"], [ 5,"Vitamin D Deficiency"], [ 298,"Weight control"]]
alergies_list = [[0, 'None'],[44,"Allergy to eggs"],[45,"Allergy to fish"], [46,"Allergy to milk"], [47,"Allergy to peanuts"], [48,"Allergy to shellfish"], [49,"Allergy to soy"], [50,"Allergy to tree nuts"], [51,"Allergy to wheat"]]
menu_13_breakfast =[["754","Vege egg roll","egg_roll-1.jpg","i2","212328"],["486","Cereals","cereal.jpg","x","140184"],["280","Banana","banana.jpg","d","32977"],["276","Apple","apple.jpg","d","591938"],["726","Tea","plain_tea.jpg","h2","2423169"]]
menu_24_breakfast =[["501","English muffins","english muffins.jpg","f","46730"],["240","Hardboilegg","boil_eggs.jpg","c1","181630"],["280","Banana","banana.jpg","d","32977"],["276","Apple","apple.jpg","d","591938"],["726","Tea","plain_tea.jpg","h2","2423169"]]
menu_1_lunch =[ ["5010","Broccoli Cheddar Soup","Cheddar-Broccoli-Soup.jpg","l","1160486"], ["5044","Salmon Baked","salmon.jpg","l","2057"],["792","Potato salad","Easy-Potato-Salad.jpg","i2","39975"],["692","Vanilla Icecream","Vanilla-ice-cream.jpg","h1","3426147"]]
menu_2_lunch =[["5031","Lentil Soup","lentil_soup.jpg","l","1411654"],["5040","Three Bean and Beef Chili","three_bean_beef.jpg","l","1220540"],["5026","Quinoa Salad","quinoa-salad.jpg","l","7029559"],["691","Chocolate Icecream","chocolate-ic-cream.jpg","h1","'17285419"]]
menu_3_lunch =[["821","Vege beef Soup","Vegetable-Beef-Soup_3.jpg","i2","111198"],["180","Turkey breast","Roasted-Turkey-Breast-3.jpg","b3","61451"],["749","Corn Salad","Corn-Salad.jpg","i2","1090431"],["692","Vanilla Icecream","Vanilla-ice-cream.jpg","h1","3426147"]]
menu_4_lunch =[["820","Tomato Soup","tomato_soup.jpg","i2","78965"],["5014","Chicken & Broccoli Stir-fry","chicken-and-broccoli-stir-fry.jpg","l","1660886"],["5041","Toasted Almond Parsley Salad","Parsley-Salad-with-Almonds.jpg","l","2661"],["691","Chocolate Icecream","chocolate-ic-cream.jpg","h1","'17285419"]]
menu_13_dinner =[["5034","Garden Vegetable Soup","vegesoup.jpg","l","27223"],["764","Hash brown potatoes","hash-brown.jpg","i2","2845672"],["657","Cheesecake","cheesecake.jpg","h1","546244"]]
menu_24_dinner =[["815","Chicken noodle soup","chick-noodle-soup.jpg","i2","11338625"],["5042","Hasselback Sweet Potatoes","hasselback-sweet-potatoes.jpg","l","3810308"],["667","Brownies","brownie.jpg","h1","50797"]]


#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
app = Flask(__name__)

#sock.connect(('127.0.0.1', 5001))
## Send some data, this method can be called multiple times
#sock.send("Twenty-five bytes to send")
## Close the socket connection, no more data transmission
#sock.close()


def check_face_match(img, current_img_path):
    faces_to_compare = []
    names = []
    for file in os.listdir("static/captures/"):
        if file.endswith(".jpg"):
            if img in file:
                pass
            else:
                names.append(file)




    # * ---------- Encode the nameless picture --------- *
    # Load picture
    face_picture = face_recognition.load_image_file(current_img_path)
    face_encoding_a1 = face_recognition.face_encodings(face_picture)
    if len(face_encoding_a1) >0:
        face_encoding_a1 = face_encoding_a1[0]


    fileName=[]


    for name in names:
        face_picture1 = face_recognition.load_image_file("static/captures/"+name)

        fileName.append(name)
        face_encoding_a2 = face_recognition.face_encodings(face_picture1)
        if len(face_encoding_a2) > 0:
            faces_to_compare.append(face_encoding_a2[0])

    matches = face_recognition.compare_faces(faces_to_compare, face_encoding_a1)

    i = 0
    for match in matches:
        if match == True:
            return match, fileName[i]
        i = i+1
    return False, "nothing"


def get_camera():
    global camera
    if not camera:
        camera = Camera()

    return camera



@app.route('/')
def root():
    return redirect(url_for('camera_start'))

@app.route('/camera_start/')
def camera_start():
    mac_say.say("Please look at me first and smile")

    return render_template('camera.html')

def gen(camera):
    while True:
        frame = camera.get_feed()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed/')
def video_feed():
    camera = get_camera()
    return Response(gen(camera),
        mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture/')
def capture():
    camera = get_camera()
    stamp = camera.capture()
    return redirect(url_for('show_capture', timestamp=stamp))

def stamp_file(timestamp):
    return 'captures/' + timestamp +".jpg"


@app.route('/capture/image/<timestamp>', methods=['POST', 'GET'])
def show_capture(timestamp):
    path = stamp_file(timestamp)
    mac_say.say("Please type in the following details")



    return render_template('userinfo_page.html',
        stamp=timestamp, path=path, data=problem_list, data1=alergies_list)

@app.route('/add_user', methods=['POST', 'GET'])
def add_user():
    if request.method == 'POST':
        result = request.form

    name = result['name']
    age = result['age']
    allergies = result['allergies']
    health = result['health']
    image = result['image']

    insertUser(name, age, allergies, health, image)
    mac_say.say("lovely. I feel like I’m your friend now. Let’s get started")
    time.sleep(2)

    #t = Thread(target=myfunc, args = (text,))
    #t.start()
    mac_say.say("Hello "+name+"I hope you are doing well today")
    time.sleep(3)
    mac_say.say("Please select one of the following options")

    return render_template('page1.html', name=name, health=health, allergies=allergies)

@app.route("/home")
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/start")
def start():

    mac_say.say("Good Afternoon. Please click on start button to continue")
    return render_template("start.html")


@app.route('/page1',methods = ['POST', 'GET'])
def page1():
    if request.method == 'POST':
        result = request.form

    return render_template("page1.html", result=result)

@app.route("/newuser")
def newuser():
    time.sleep(1)
    camera = get_camera()
    stamp = camera.captureforaldreadyuser()

    stamp1 = "static/captures/test.jpg"


    flag, name = check_face_match(stamp, stamp1)


    rv = getUser(name)
    id = 0

    for r in rv:
        name = r[0]
        health = r[1]
        allergies = r[2]
        id = r[3]

    if 'id' in session:
        session['id'] = id
    else:
        session['id'] = id



    if flag == True:
        mac_say.say("Hello"+name)
        time.sleep(1)
        mac_say.say("I have missed seeing you. How are you today?")
        time.sleep(2)
        mac_say.say("I hope you are having a wonderful day.")
        time.sleep(2)
        mac_say.say("Please select one of the following options")
        return render_template("page1.html", name = name, health = health, allergies=allergies  )
    else:
        mac_say.say("I see that we are meeting first time")
        time.sleep(2)
        mac_say.say("Please click the button if you like to be my friend?")
        return render_template("newuser.html")


@app.route("/saveChoice/<name>", methods=['POST', 'GET'])
def saveChoice(name):
    today = datetime.today()
    name = name
    image = name+".jpg"
    user = session['id']

    addFood(name, image, user, today)
    mac_say.say("nice choice. i like"+name+"too")
    time.sleep(1)
    mac_say.say("Please click to end the session")
    return render_template("userfood.html", name=name, image=image)


@app.route("/previousfood/")
def previousfood():

    user = session['id']

    rv={}
    rv = getFood(user)

    return render_template("previousfood.html", data=rv)




@app.route("/menu_page/<health>", methods=['POST', 'GET'])
def menu_page(health):

    user = health.split('-')
    health = user[0]
    allergies = user[1]
    today = datetime.today()
    day=datetime.today().weekday()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    timee = current_time.split(':')
    time = int(timee[0])
    dayyy = type(day)
    menu =[]
    #print(time)
    #menu= menu_24_breakfast[4]
    print("Current Time =", time)
    print("Today's day:", day)
    #if day == 1 and  time<2:
    if day == 0 and (time > 8 and time < 12):
        menu = menu_13_breakfast
    elif day == 1 and (time > 8 and time < 12):
        menu = menu_24_breakfast
    elif (day == 2 or day == 5) and (time > 8 and time < 12):
        menu = menu_13_breakfast
    elif (day == 3 or day == 4) and (time > 8 and time < 12):
        menu = menu_24_breakfast
    elif (day == 0 or day == 4) and (time > 12 and time < 18):
        menu = menu_24_dinner
    elif day == 1 and (time > 12 and time < 18):
        menu = menu_2_lunch
    elif (day == 2 or day == 5) and (time > 12 and time < 18):
        menu = menu_3_lunch
    elif day == 3 and (time > 12 and time < 18):
        menu = menu_13_dinner
    elif (day == 0 or day == 4) and (time > 18 and time < 23):
        menu = menu_24_dinner
    elif (day == 2 or day == 5) and (time > 18 and time < 23):
        menu = menu_13_dinner
    elif (day == 3 or day == 1) and (time > 18 and time < 23):
        menu = menu_24_dinner
    else:
        menu = menu_13_dinner

    mac_say.say("let’s talk about your todays meal. I see that you had the following menu today, you will need to select one to check the nutritions")


    return render_template("menu_page.html", health=health, allergies=allergies, menu=menu)


@app.route("/userinfo_page")
def userinfo_page():

	return render_template("userinfo_page.html", data=problem_list)


@app.route("/interaction_page")
def interaction_page():
    engine = pyttsx3.init()
    engine.say("i am in interaction page")
    engine.runAndWait()
    return render_template("interaction_page.html")

@app.route("/menu_page/nutritions_page/<health>", methods=['POST', 'GET'])
def nutritions_page(health):
    h = health.split('-')
    health_id = h[0]
    allergy = h[1]
    item = h[2]
    fg =h[3]
    food_id = h[4]

    nut = fs.food_get(food_id)
    serve = nut['servings']
    serve = serve['serving']


    data = {}

    if len(serve) > 1:

        data =  {
                'calories' : serve['calories'],
                'carbohydrates' : serve['carbohydrate'],
                'fat' : serve['fat'],

                'protein' : serve['protein']
             }
    else:
        data =  {
                'calories' : serve['calories'],
                'carbohydrates' : serve['carbohydrate'],
                'fat' : serve['fat'],

                'fiber' : serve['fiber'],
                'protein' : serve['protein']
             }

    mac_say.say("Oh, nice. I like soups too")
    time.sleep(1)
    #mac_say.say("Remember you had turkey breast with corn salad last time when we interacted.")
    #mac_say.say("Remember you had vegetable soup last time when we interacted.")

    time.sleep(3)
    mac_say.say("Lets have a look at its nutrition value now")

    return render_template("nutritions_page.html",  serve =data, health=health)

@app.route("/menu_page/nutritions_page/suggestions_page/<health>", methods=['POST', 'GET'])
def suggestions_page(health):
    h = health.split('-')
    health_id = h[0]
    allergy = h[1]
    item = h[2]
    fg =h[3]
    food_id = h[4]

    url_goodfor='https://api.nutridigm.com/api/v1/nutridigm/goodfor?subscriptionId=123&itemID='+item+'&problemId='+str(health_id)
    url_topitemstoconsume='https://api.nutridigm.com/api/v1/nutridigm/topitemstoconsume?subscriptionId=123&problemId='+str(health_id)
    url_thingstoavoid='https://api.nutridigm.com/api/v1/nutridigm/topitemstoavoid?subscriptionId=123&problemId='+str(health_id)
    url_suggest='https://api.nutridigm.com/api/v1/nutridigm/suggest?subscriptionId=123&problemId='+str(health_id)+'&fg2='+str(fg)

    resp = requests.get(url_goodfor)
    resp_top = requests.get(url_topitemstoconsume)
    resp_avoid = requests.get(url_thingstoavoid)
    resp_suggest = requests.get(url_suggest)

    json_data = resp.json()
    json_top = resp_top.json()
    json_avoid = resp_avoid.json()
    json_suggest = resp_suggest.json()
    notes = json_data['notes']
    print(json_data)

    data = {
             #'goodfor_data': resp.json(),
             'topitemstoconsume_data': resp_top.json(),
             'thingstoavoid_data' : resp_avoid.json(),
             #'suggestions_data' : resp_suggest.json()
         }


    if resp.status_code != 200:
        # This means something went wrong.
        raise ApiError('GET /tasks/ {}'.format(resp.status_code))

    #mac_say.say("You see that your selected item has 10 calories while it does not have any carbs, fat or proteins")
    mac_say.say("You see that your selected item has 170 calories while it has 20 grams of carbs, 4 grams of fat and 14 grams of proteins")
    time.sleep(1)
    mac_say.say("Please click on the button to get some of my suggestions")

    return render_template("suggestions_page.html", data=data)
@app.route("/menu_page/nutritions_page/suggestions_page/response")
def response():
    #mac_say.say("this soup is very healthy. It will be helpful to keep you fit.")
    mac_say.say("You should try to consume Chicken noodle soup less.It will be helpful to keep you fit.")
    time.sleep(1)
    mac_say.say("Although, I suggest you to exercise more and eat Broccoli, Carrots, Potatoes, Spinach, Flaxseed, Nuts, Fish, Beans, Avocado, Persimmons and Berries")
    time.sleep(2)
    mac_say.say("while i recommend you to avoid more than 2 alcoholic drinks in a day, Sweets and Refined sugar, Excess Weight, Animal fat & Hydrogenated Vegetable Oil, Processed Meats and strictly avoid Smoking;")
    time.sleep(1)
    mac_say.say("Do you think you can do this for yourself?")
    time.sleep(4)
    mac_say.say("great")
    time.sleep(1)
    mac_say.say("Now, Please select your preference about today's meal after listening to my suggestions")

    return render_template("response.html")
@app.route("/menu_page/nutritions_page/suggestions_page/response/options")
def options():

    mac_say.say("thank you")
    time.sleep(2)
    mac_say.say("Now Please Click on one of the following food Option that you would like to eat next time")

    return render_template("options.html")

@app.route("/end_page")
def end_page():
    mac_say.say("I really appreciate your time, Please fill the survey at the end of this session too")
    time.sleep(1)
    mac_say.say("I Hope to see you again")
    mac_say.say("bye bye")
    return render_template("end_page.html")


if __name__ == "__main__":
    app.secret_key = 'SECRET KEY'
    app.run(debug = True)
