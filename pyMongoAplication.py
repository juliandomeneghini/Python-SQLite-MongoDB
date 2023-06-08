import pprint
import pymongo as pyM
import datetime

client = pyM.MongoClient("mongodb+srv://juliandomeneghini:yHKT5BRQGj9BU2cU@cluster0.kxtnyi0.mongodb.net/?retryWrites"
                         "=true&w=majority")

db = client.test
collections = db.test.collections
print(db.list_collection)

# definição do info para comport o doc
post = {
    "author": "Julian",
    "text": "Integration Python with SQLite and MongoDB",
    "tags": ["python3", "pymongo, SQLite, MongoDB"],
    "date": datetime.datetime.utcnow()
}

# preparando para submeter as infos
posts = db.posts
post_id = posts.insert_one(post).inserted_id
print(post_id)


print(db.posts.find_one())

pprint.pprint(db.posts.find_one())

# bulk inserts
new_posts = [{
            "author": "Julian",
            "endereco": "Rua tiradentes",
            "cpf": "362689450",
            "date": datetime.datetime.utcnow()},
            {
            "author": "Janaina",
            "endereco": "Rua Oswald Aranha",
            "cpf": "567890987",
            "date": datetime.datetime.utcnow()},
            {
            "author": "Pietro",
            "endereco": "Rua Noes",
            "cpf": "874567890",
            "date": datetime.datetime.utcnow()}]

result = posts.insert_many(new_posts)
print(result.inserted_ids)

print("\nRecuperação final ")
pprint.pprint(db.posts.find_one({"author": "Janaina"}))

print("\n Documentos presentes na coleção posts!")
for post in posts.find():
    pprint.pprint(post)
