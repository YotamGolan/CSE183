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
from PIL import Image

@unauthenticated("index", "index.html")
def index():
    commHolder = DBComm('Yotam','','canvasDB',)
    holder = commHolder.selectPixelMatrix(0)
    width, height = 500, 500
    desc = (height, width, 3)
    mat = np.zeros(desc, dtype = np.uint8)
    for row in holder:
        mat[row[2], row[3]] = [row[4],row[5],row[6]]
    i = Image.fromarray(mat, "RGB")
    i.show()
    return dict()
