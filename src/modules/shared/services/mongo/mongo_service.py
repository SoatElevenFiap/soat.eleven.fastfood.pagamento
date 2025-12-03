from pymongo import AsyncMongoClient

class MongoService:
    def __init__(self, connection_string: str, database_name: str = "payments"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = AsyncMongoClient(self.connection_string)
        self.db = self.client[database_name]

    async def add_document(self, collection_name: str, document: dict):
        collection = self.db[collection_name]
        await collection.insert_one(document)

    async def get_document(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        return await collection.find_one(query)

    async def update_document(self, collection_name: str, query: dict, document: dict):
        collection = self.db[collection_name]
        await collection.update_one(query, {'$set': document})

    async def delete_document(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        await collection.delete_one(query)

    async def close(self):
        await self.client.close()


