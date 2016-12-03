# Define your tables below (or better in another model file) for example
#
# >>> db.define_table('mytable', Field('myfield', 'string'))
#
# Fields can be 'string','text','password','integer','double','boolean'
#       'date','time','datetime','blob','upload', 'reference TABLENAME'
# There is an implicit 'id integer autoincrement' field
# Consult manual for more options, validators, etc.

import datetime


db.define_table('dateContent',
                Field('dateEvent', 'text'),
                Field('dateDay', 'integer'),
                Field('dateMonth', 'integer'),
                Field('dateYear', 'integer'),
                )

db.define_table('post',
                Field('user_email', default=auth.user.email if auth.user_id else None),
                Field('post_content', 'text'),
                Field('created_on', 'datetime', default=datetime.datetime.utcnow()),
                Field('updated_on', 'datetime', update=datetime.datetime.utcnow()),
                )

db.define_table('intern',
                Field('title'),
                Field('organization'),
                Field('description', 'text'),
                Field('requirements', 'text'),
                Field('due_date'),
                Field('upload', 'datetime', default=datetime.datetime.utcnow()),
                Field('uploader', default=auth.user.email if auth.user_id else None)
                )

db.define_table('fav',
                Field('title'),
                Field('organization'),
                Field('description', 'text'),
                Field('requirements', 'text'),
                Field('due_date'),
                Field('upload', 'datetime', default=datetime.datetime.utcnow()),
                Field('uploader', default=auth.user.email if auth.user_id else None)
                )


db.intern.id.readable = False
db.intern.title.requires = IS_NOT_EMPTY()
db.intern.organization.requires = IS_NOT_EMPTY()
db.intern.description.requires = IS_NOT_EMPTY()
db.intern.due_date.requires = IS_NOT_EMPTY()
db.intern.upload.readable = db.intern.upload.writable = False
db.intern.uploader.readable = db.intern.uploader.writable = False

# I don't want to display the user email by default in all forms.
db.post.user_email.readable = db.post.user_email.writable = False
db.post.post_content.requires = IS_NOT_EMPTY()
db.post.created_on.readable = db.post.created_on.writable = False
db.post.updated_on.readable = db.post.updated_on.writable = False

#from calender
db.dateContent.dateDay.writable = False
db.dateContent.dateMonth.writable = False
db.dateContent.dateYear.writable = False

# after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
