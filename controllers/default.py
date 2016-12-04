# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

# -------------------------------------------------------------------------
# This is a sample controller
# - index is the default action of any application
# - user is required for authentication and authorization
# - download is for downloading files uploaded in the db (does streaming)
# -------------------------------------------------------------------------

# Start of a calender implantation modified from python.about.com

import re, datetime, calendar

year = ['January',
        'February'
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December']

def get_user_name_from_email(email):
    """Returns a string corresponding to the user first and last names,
    given the user email."""
    u = db(db.auth_user.email == email).select().first()
    if u is None:
        return 'None'
    else:
        return ' '.join([u.first_name, u.last_name])


def index():
     """
     This is your main controller.
     """
    # I am creating a bogus list here, just to have some divs appear in the
    # view.  You need to read at most 20 posts from the database, in order of
    # most recent first, and you need to return that list here.
    # Note that posts is NOT a list of strings in your actual code; it is
    # what you get from a db(...).select(...).
    # posts = ['banana', 'pear', 'eggplant']
     return dict(posts=db().select(orderby=~db.intern.upload), author = get_user_name_from_email,
                favs=db().select(orderby=~db.fav.upload), inProg=db().select(orderby=~db.inProg.upload))
@auth.requires_login()
def calender():
    # Sets today equal to  year-month-date, then separates the three values
    today = datetime.datetime.date(datetime.datetime.now())

    current = re.split('-', str(today))
    todayNo = int(current[1])
    todayMonth = year[todayNo - 2]
    todayDay = int(re.sub('\A0', '', current[2]))  # Date time returns 2 digit number, but we want 1 digit for 1-9
    todayYear = int(current[0])
    month = calendar.monthcalendar(todayYear, todayNo)
    nWeeks = len(month)

    week = None
    day = None

    # Loads in calender content from the database
    dateContent = db(db.dateContent).select()
    return dict(todayMonth=todayMonth, todayYear=todayYear, todayDay=todayDay, nWeeks=nWeeks, month=month,
                dateContent=dateContent)


@auth.requires_login()
def add():
    # This implements the ability to add events to calender dates
    date = request.args(0)
    db.dateContent.dateDay.default = date
    form = SQLFORM(db.dateContent)

    if form.process().accepted:
        session.flash = T('Event Created!')
        redirect(URL('default', 'index'))
    return dict(form=form)


@auth.requires_login()
def edit_internship():
    """
    This is the page to create / edit / delete a post.
    """

    if request.args(0) is None:
        form_type = 'create'
        form = SQLFORM(db.intern)

    else:
        q = ((db.intern.uploader == auth.user.email)&
             (db.intern.id == request.args(0)))
        cl = db(q).select().first()
        if cl is None:
            session.flash = T('Not Authorized')
            redirect(URL('default','index'))

        is_edit = (request.vars.edit == 'true')
        form_type = 'edit' if is_edit else 'view'
        form = SQLFORM(db.intern, record=cl, deletable=True, readonly=not True)

    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'edit_internship', args=[cl.id])))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        #button_list.append(A('Edit', _class='btn btn-warning',
         #                    _href=URL('default', 'edit_internship', args=[cl.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))
    if form.process().accepted:
        if form_type == 'create':
            session.flash = T('Internship added.')
        else:
            session.flash = T('Internship edited.')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('Please enter correct values.')

    return dict(form=form, button_list=button_list)


def view_internship():
    """
    This is the page to view the internship information
    """


    if request.args(0) is None:
        redirect(URL('default', 'index'))

    #else:
    q = (db.intern.id == request.args(0))
    cl = db(q).select().first()

    is_edit = (request.vars.edit == 'true')
    form_type = 'view'
    form = SQLFORM(db.intern, record=cl, deletable=False, readonly=not False)

    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'edit_internship', args=[cl.id])))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        #button_list.append(A('Edit', _class='btn btn-warning',
         #                    _href=URL('default', 'edit_internship', args=[cl.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))
    if form.process().accepted:
        if form_type == 'create':
            session.flash = T('Internship added.')
        else:
            session.flash = T('Internship edited.')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('Please enter correct values.')

    return dict(form=form, button_list=button_list, post=db(db.intern.id == request.args(0)).select().first())

def view_internshipFav():
    """
    This is the page to view the internship information
    """


    if request.args(0) is None:
        redirect(URL('default', 'index'))

    #else:
    q = (db.fav.id == request.args(0))
    cl = db(q).select().first()

    is_edit = (request.vars.edit == 'true')
    form_type = 'view'
    form = SQLFORM(db.fav, record=cl, deletable=False, readonly=not False)

    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'edit_internship', args=[cl.id])))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        #button_list.append(A('Edit', _class='btn btn-warning',
         #                    _href=URL('default', 'edit_internship', args=[cl.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))
    if form.process().accepted:
        if form_type == 'create':
            session.flash = T('Internship added.')
        else:
            session.flash = T('Internship edited.')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('Please enter correct values.')

    return dict(form=form, button_list=button_list, post=db(db.fav.id == request.args(0)).select().first())

def view_internshipInProg():
    """
    This is the page to view the internship information
    """


    if request.args(0) is None:
        redirect(URL('default', 'index'))

    #else:
    q = (db.inProg.id == request.args(0))
    cl = db(q).select().first()

    is_edit = (request.vars.edit == 'true')
    form_type = 'view'
    form = SQLFORM(db.inProg, record=cl, deletable=False, readonly=not False)

    button_list = []
    if form_type == 'edit':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'edit_internship', args=[cl.id])))
    elif form_type == 'create':
        button_list.append(A('Cancel', _class='btn btn-warning',
                             _href=URL('default', 'index')))
    elif form_type == 'view':
        #button_list.append(A('Edit', _class='btn btn-warning',
         #                    _href=URL('default', 'edit_internship', args=[cl.id], vars=dict(edit='true'))))
        button_list.append(A('Back', _class='btn btn-primary',
                             _href=URL('default', 'index')))
    if form.process().accepted:
        if form_type == 'create':
            session.flash = T('Internship added.')
        else:
            session.flash = T('Internship edited.')
        redirect(URL('default', 'index'))
    elif form.errors:
        session.flash = T('Please enter correct values.')

    return dict(form=form, button_list=button_list, post=db(db.inProg.id == request.args(0)).select().first())

def add_fav():
    id = request.args(0)
    db.fav.insert(title=db.intern(id).title, organization=db.intern(id).organization)
    response.flash = "Added to Favorites"

    return True

def add_favFromProg():
    id = request.args(0)
    db.fav.insert(title=db.inProg(id).title, organization=db.inProg(id).organization)
    response.flash = "Added to Favorites"
    redirect(URL('default', 'index'))


    return True


def add_progFromFave():
    id = request.args(0)
    db.inProg.insert(title=db.fav(id).title, organization=db.fav(id).organization)
    response.flash = "Added to Favorites"
    redirect(URL('default', 'index'))


    return True


def add_inProg():
    id = request.args(0)
    db.inProg.insert(title=db.intern(id).title, organization=db.intern(id).organization)
    response.flash = "Added to In Progress"
    return True

def del_fav():
    delID= request.args(0)
    db(db.fav.id == delID).delete()
    return True

def del_inProg():
    delID= request.args(0)
    db(db.inProg.id == delID).delete()
    return True

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
def main():
    return dict(posts=db().select(orderby=~db.intern.upload), author=get_user_name_from_email,
                favs=db().select(orderby=~db.fav.upload), inProg=db().select(orderby=~db.inProg.upload))

