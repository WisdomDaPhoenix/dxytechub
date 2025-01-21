def addToMongoDB(student_document):
    from pymongo.mongo_client import MongoClient
    from pymongo.server_api import ServerApi

    uri = "mongodb+srv://iconsoftwareguru:%40Datron24@dxyserverlessdb.ngiqf.mongodb.net/?retryWrites=true&w=majority&appName=DXYServerlessDB"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client['dxy']
    students = db['students']
    result = students.insert_one(student_document)
    if result.inserted_id:
        return f"Your assigned Client ID: {result.inserted_id}"
    return f"You have no assigned Client ID. Contact Admin"

#
# if __name__=="__main__":
#     print(addToMongoDB())