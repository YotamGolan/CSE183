"""
This file defines actions, i.e. functions the URLs are mapped into
The @action(path) decorator exposed the function at URL:

    http://127.0.0.1:8000/{app_name}/{path}

If app_name == '_default' then simply

    http://127.0.0.1:8000/{path}

If path == 'index' it can be omitted:

    http://127.0.0.1:8000/

The path follows the bottlepy syntax.

@action.uses('generic.html')  indicates that the action uses the generic.html template
@action.uses(session)         indicates that the action uses the session
@action.uses(db)              indicates that the action uses the db
@action.uses(T)               indicates that the action uses the i18n & pluralization
@action.uses(auth.user)       indicates that the action requires a logged in user
@action.uses(auth)            indicates that the action requires the auth object

session, db, T, auth, and tempates are examples of Fixtures.
Warning: Fixtures MUST be declared with @action.uses({fixtures}) else your app will result in undefined behavior
"""

from py4web import action, request, abort, redirect, URL
from yatl.helpers import A
from .common import db, session, T, cache, auth, logger, authenticated, unauthenticated, flash
from .dbcomm import *
import numpy as np
from py4web.utils.url_signer import URLSigner
from PIL import Image
import io
import base64

url_signer = URLSigner(session)

def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def pil_to_dataurl(img):
    #converts PIL image to dataurl
    data = io.BytesIO()
    img.save(data, "png")
    data64 = base64.b64encode(data.getvalue())
    return u'data:img/png;base64,'+data64.decode('utf-8')

@action('index')
@action.uses(auth.user, url_signer, 'index.html')
def index():
    commHolder = DBComm('Yotam','','canvasDB',)
    holder = commHolder.selectPixelMatrix(0)
    width, height = 750, 750
    desc = (height, width, 3)
    mat = np.zeros(desc, dtype=np.uint8)
    for row in holder:
        mat[row[2], row[3]] = [row[4],row[5],row[6]]
    i = Image.fromarray(mat, "RGB")
    #i.show()
    return dict(
        load_image_url=URL('load_image', signer=url_signer),
        set_pixel_url=URL('set_pixel', signer=url_signer),
        add_user_url=URL('add_user', signer=url_signer),
    )

@action('load_image')
@action.uses(url_signer.verify())
def load_image():
    commHolder = DBComm('Yotam','','canvasDB',)
    holder = commHolder.selectPixelMatrix(0)
    width, height = 750, 750
    desc = (height, width, 3)
    #a = np.array([255,255,255])
    #a = a.reshape(3,1)
    mat = np.zeros(desc, dtype=np.uint8)
    for row in holder:
        mat[row[3], row[2]] = [row[4], row[5], row[6]]
    i = Image.fromarray(mat, "RGB")
    #i.show()
    return dict(
        image=pil_to_dataurl(i),
    )

@action('set_pixel', method="POST")
@action.uses(url_signer.verify())
def set_image():
    user_email = get_user_email()
    x = request.json.get('x')
    y = request.json.get('y')
    r = request.json.get('r')
    g = request.json.get('g')
    b = request.json.get('b')
    commHolder = DBComm('Yotam','','canvasDB',)
    #print(x, y, r, g, b)
    id = commHolder.selectUserData(user_email)
    #print(id[0][0])
    commHolder.insertPixel(id[0], x, y, r, g, b)
    message = "success"
    return dict(message=message)

@action('add_user', method=["GET","POST"])
@action.uses(url_signer.verify())
def add_user():
    # The idea is to add the current user to the database when the index page is loaded.
    # This should have the effect of adding the user if they are new,
    # and doing nothing if they already exist (since email is unique).
    email = get_user_email()
    firstName = auth.current_user.get('first_name') if auth.current_user else None
    lastName = auth.current_user.get('last_name') if auth.current_user else None
    pixelCount = 20
    print("adding user")
    commHolder = DBComm('Yotam','','canvasDB',)
    try:
        commHolder.insertUser(email, firstName, lastName, pixelCount)
        print("user added")
    except:
        print("user already exists")
    
    return dict()

# profile page stuff
@action('profile')
@action.uses(auth.user, url_signer, 'profile.html')
def profile():
    commHolder = DBComm('Yotam','','canvasDB',)
    email = get_user_email()
    username = auth.current_user.get('username') if auth.current_user else None
    firstname = auth.current_user.get('first_name') if auth.current_user else None
    lastname = auth.current_user.get('last_name') if auth.current_user else None
    
    user = commHolder.selectUserData(email)
    pixelsremaining = user[4]
    
    return dict(email=email,
                username=username,
                firstname=firstname,
                lastname=lastname,
                pixelsremaining=pixelsremaining,
                load_users_image_url=URL('load_users_image', signer=url_signer),
                load_image_url=URL('load_image', signer=url_signer),
               )

@action('load_users_image')
@action.uses(url_signer.verify())    
def load_users_image():
    commHolder = DBComm('Yotam','','canvasDB',)
    user_email = get_user_email()
    print(user_email)
    # NEED TO GET ACTUAL USERS INSERTED INTO THE USER TABLE
    user_id = commHolder.selectUserData(user_email)[0]
    print(user_id)
    
    holder = commHolder.selectPixelsByUser(user_id)
    
    width, height = 750, 750
    desc = (height, width, 3)
    
    mat = np.zeros(desc, dtype=np.uint8)
    for row in holder:
        mat[row[3], row[2]] = [row[4], row[5], row[6]]
    i = Image.fromarray(mat, "RGB")
    
    return dict(
        image=pil_to_dataurl(i),
    )




