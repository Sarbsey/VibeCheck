from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os

def format_data(user_info, token_data):
    name = user_info['display_name']
    name = name.split()
    user_id = user_info['id']
    FirstName = name[0]
    LastName = name[1:]

    submit = {"data":{
    "user_id" : user_id,
    ""
    "user_data":{
        "FirstName":FirstName,
        "LastName":LastName
            },
    "token_data": token_data
        }
    }

    return submit


def submit(data_submit):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )
    doc_uid = fc.query(q.new_id())


    fc.query(
    q.create(
    q.ref(
    q.collection('spotvac_users'), doc_uid), data_submit
    ))
    return


def length():
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )

    length = fc.query(
    q.count(
    q.paginate(
    q.documents(
    q.collection('spotvac_users')))))

    db_length = length['data'][0]
    return db_length

def look_up(user_id):
    fc = FaunaClient(
    secret=os.environ['fauna_secret'],
    endpoint="https://db.fauna.com/"
    )

    fdb_user_search = fc.query(
    q.paginate(q.match(
    q.index("test2"), user_id)) 
    )
    
    fdb_search_results = fdb_user_search['data']

    user_verification_data = fc.query(
        q.map_(
        q.lambda_("name", q.get(q.var("name"))),
        fdb_search_results
    ))

    return user_verification_data