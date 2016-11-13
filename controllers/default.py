# -*- coding: utf-8 -*-


# Start of a calender implantation modified from python.about.com

import re, datetime, calendar

year = ['January', 
		'February', 
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

def index():
    # Sets today equal to  year-month-date, then separates the three values
    today = datetime.datetime.date(datetime.datetime.now())

    current = re.split('-', str(today))
    todayNo = int(current[1])
    todayMonth = year[todayNo - 1]
    todayDay = int(re.sub('\A0', '', current[2]))   # Date time returns 2 digit number, but we want 1 digit for 1-9
    todayYear = int(current[0])
    month = calendar.monthcalendar(todayYear, todayNo)
    nWeeks = len(month)

    week = None
    day = None
    

    return dict(todayMonth=todayMonth, todayYear=todayYear, todayDay=todayDay, nWeeks=nWeeks, month=month)


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


