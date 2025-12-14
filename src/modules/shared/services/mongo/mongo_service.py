from typing import Optional

from bson import ObjectId
from pymongo import AsyncMongoClient


class MongoService:
    def __init__(self, connection_string: str, database_name: str = "payments"):
        self.connection_string = connection_string
        self.database_name = database_name
        self.client = AsyncMongoClient(self.connection_string)
        self.db = self.client[database_name]

    async def add_document(self, collection_name: str, document: dict) -> str:
        collection = self.db[collection_name]
        operation = await collection.insert_one(document)
        return str(operation.inserted_id)

    async def get_document(self, collection_name: str, query: dict) -> dict | None:
        if "id" in query:
            query["_id"] = (
                ObjectId(query["id"]) if ObjectId.is_valid(query["id"]) else query["id"]
            )
            del query["id"]
        collection = self.db[collection_name]
        document = await collection.find_one(query)
        if document and "_id" in document:
            document["_id"] = str(document["_id"])
        return document if document else None

    async def update_document(
        self, collection_name: str, query: dict, document: dict
    ) -> Optional[dict]:
        if "id" in query:
            query["_id"] = (
                ObjectId(query["id"]) if ObjectId.is_valid(query["id"]) else query["id"]
            )
            del query["id"]
        collection = self.db[collection_name]
        await collection.update_one(query, {"$set": document})
        return await self.get_document(collection_name, query)

    async def get_all_documents(
        self, collection_name: str, query: dict = None
    ) -> list[dict]:
        collection = self.db[collection_name]
        query = query or {}
        if "id" in query:
            query["_id"] = (
                ObjectId(query["id"]) if ObjectId.is_valid(query["id"]) else query["id"]
            )
            del query["id"]
        cursor = collection.find(query)
        documents = []
        async for document in cursor:
            if document and "_id" in document:
                document["_id"] = str(document["_id"])
            documents.append(document)
        return documents

    async def delete_document(self, collection_name: str, query: dict):
        collection = self.db[collection_name]
        await collection.delete_one(query)

    async def close(self):
        await self.client.close()
