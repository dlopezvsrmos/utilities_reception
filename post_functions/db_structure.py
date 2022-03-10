import pymongo


client = pymongo.MongoClient(f"mongodb+srv://mos-reception:m0X1mKSuxyWCdfks@cluster0.fs8pd.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
database = client["utilities"]

properties_col = database["properties"]
vendors_col = database["vendors"]
