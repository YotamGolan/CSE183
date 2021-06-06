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
from .common import db, session, T, cache, auth, logger , flash
from .dbcomm import *
import numpy as np
from py4web.utils.url_signer import URLSigner
from PIL import Image
import io
import base64
from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import math
from numpy import array

from nqgcs import NQGCS
BUCKET = '/checkpointing'
GCS_KEY_PATH = os.path.join(APP_FOLDER, 'private/gcs_keys.json')
PIC_LOC_PATH = os.path.join(APP_FOLDER, 'tmp/')
CRED_PATH = os.path.join(APP_FOLDER, "private/credentials.json")
credentials = json.load(open(CRED_PATH))
commHolder = DBComm(credentials['name'],credentials['password'],credentials['database'])

with open(GCS_KEY_PATH) as gcs_key_f:
    GCS_KEY = json.load(gcs_key_f)

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
        decr_pixel_count_url=URL('decr_pixel_count', signer=url_signer),
        get_pixel_count_url=URL('get_pixel_count', signer=url_signer),
    )

def createImage():
    checkpointID = commHolder.getLargestID()
    checkpointID = int(math.floor(checkpointID / 500.0)) * 500
    

    holder = commHolder.selectPixelMatrix(checkpointID)

    mat = retrieveCheckpoint()
    
    for row in holder:
        mat[row[3], row[2]] = [row[4], row[5], row[6]]
    i = Image.fromarray(mat, "RGB")
    return i

@action('load_image')
@action.uses(url_signer.verify())
def load_image():
    i = createImage()
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
    currentID = commHolder.getLargestID()
    #print(currentID)
    
    #print(x, y, r, g, b)
    id = commHolder.selectUserData(user_email)
    #print(id[0][0])
    commHolder.insertPixel(id[0], x, y, r, g, b)
    if(currentID%500 == 0):
        checkpoint()
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
    userHolder = commHolder.selectUserData(email)
    if(len(userHolder) == 0):
        commHolder.insertUser(email, firstName, lastName, pixelCount)   
    
    return dict()

# profile page stuff
@action('profile')
@action.uses(auth.user, url_signer, 'profile.html')
def profile():
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
    user_email = get_user_email()
    #print(user_email)
    # NEED TO GET ACTUAL USERS INSERTED INTO THE USER TABLE
    user_id = commHolder.selectUserData(user_email)[0]
    #print(user_id)
    
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

@action('decr_pixel_count', method=["GET","POST"])
@action.uses(auth.user, url_signer)
def decr_pixel_count():
    user_email = get_user_email()
    user = commHolder.selectUserData(user_email)
    pixel_count = request.json.get('pixel_count')
    commHolder.setPixelCount(user[0],pixel_count)
    #pixel_count = user[4]
    #commHolder.decrementPixelCount(user[0])
    return dict(
        #pixel_count=pixel_count,
    )

@action('get_pixel_count', method=["GET","POST"])
@action.uses(auth.user, url_signer)
def get_pixel_count():
    user_email = get_user_email()
    user = commHolder.selectUserData(user_email)
    pixel_count = user[4]
    print(pixel_count)
    return dict(
        pixel_count=pixel_count,
    )

# private line canvas
@action('private')
@action.uses(auth.user, url_signer, 'private.html')
def private():
    return dict()

def checkpoint():
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(GCS_KEY)
    client = storage.Client(credentials=credentials, project='collabcanvas')
    bucket = client.get_bucket('checkpointing')
     

    checkpointID = commHolder.getLargestID()
    checkpointID = int(math.floor(checkpointID / 500.0)) * 500
    picName = 'checkpoint'+str(checkpointID)+'.png'

    imgMatrix = retrieveCheckpoint(checkpointID = checkpointID-1)
    holder = commHolder.selectPixelMatrix(checkpointID-3)
    for row in holder:
        imgMatrix[row[3], row[2]] = [row[4], row[5], row[6]]
    tempImage = Image.fromarray(imgMatrix, "RGB")

    picLoc = PIC_LOC_PATH + picName
    tempImage.save(picLoc)
    blob = bucket.blob(picName)
    blob.upload_from_filename(picLoc)
    os.remove(picLoc) 
    return()

def retrieveCheckpoint(checkpointID = None):
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(GCS_KEY)
    client = storage.Client(credentials=credentials, project='collabcanvas')
    bucket = client.get_bucket('checkpointing')

    if(checkpointID==None):
        checkpointID = commHolder.getLargestID()
        
    checkpointID = (int(math.floor(checkpointID / 500.0)) * 500) 
    picName = 'checkpoint' + str(checkpointID) +'.png'
    picLoc = PIC_LOC_PATH + picName
    
    try: 
        blob = bucket.blob(picName)
        blob.download_to_filename(picLoc)
        image = Image.open(picLoc)  
        picArray = array(image)
        image.close()
        os.remove(picLoc)
    except:
        width, height = 750, 750
        desc = (height, width, 3)
        picArray = np.zeros(desc, dtype=np.uint8)

    return(picArray)


