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

user_id = "1234"
FirstName = "4321"
LastName = "098"
doc_uid = client.query(q.new_id())

submit = {"data":{
    "user_id" : user_id,
    "user_data":{
        "FirstName":FirstName,
        "LastName":LastName
    }
}
}
client.query(
    q.create(
        q.ref(
            q.collection('spotvac_users'), doc_uid), submit
        )
)


#indexes = client.query(q.get(q.ref(q.collection("spotvac_users"), "1")))

#print(indexes)