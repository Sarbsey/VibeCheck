from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
import os
from dotenv import load_dotenv

load_dotenv()

client = FaunaClient(
  secret=os.environ['fauna_secret'],
  # NOTE: Use the correct endpoint for your database's Region Group.
  endpoint="https://db.fauna.com/",
)

user_id = "ggggg"
FirstName = "vvvvvvv"
LastName = "ffff"
doc_uid = client.query(q.new_id())

submit = {"data":{
    "user_id" : user_id,
    "user_data":{
        "FirstName":FirstName,
        "LastName":LastName
    }
}
}
length = client.query(
    q.count(
        q.paginate(
                q.documents(
                    q.collection('spotvac_users')
                )
            )
        )
)

print(length['data'][0])

#indexes = client.query(q.get(q.ref(q.collection("spotvac_users"), "1")))

#print(indexes)