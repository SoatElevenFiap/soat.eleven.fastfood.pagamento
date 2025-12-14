from unittest.mock import AsyncMock, MagicMock

import pytest
from bson import ObjectId
from pytest_mock import MockFixture

from modules.shared.services.mongo.mongo_service import MongoService


@pytest.mark.asyncio
class TestMongoService:
    @pytest.fixture
    def mongo_service(self) -> MongoService:
        return MongoService(
            connection_string="mongodb://localhost:27017", database_name="test_db"
        )

    @pytest.fixture
    def mock_collection(self, mocker: MockFixture):
        mock_collection = MagicMock()
        mock_collection.insert_one = AsyncMock()
        mock_collection.find_one = AsyncMock()
        mock_collection.update_one = AsyncMock()
        mock_collection.find = MagicMock()
        mock_collection.delete_one = AsyncMock()
        return mock_collection

    @pytest.fixture
    def mock_db(self, mocker: MockFixture, mock_collection: MagicMock):
        mock_db = MagicMock()
        mock_db.__getitem__ = MagicMock(return_value=mock_collection)
        return mock_db

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_add_document_successfully(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        document = {"name": "test", "value": 123}
        inserted_id = ObjectId()

        mock_collection.insert_one.return_value = MagicMock(inserted_id=inserted_id)
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.add_document(collection_name, document)

        mock_collection.insert_one.assert_called_once_with(document)
        assert result == str(inserted_id)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_document_successfully(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        query = {"name": "test"}
        document = {"_id": ObjectId(), "name": "test", "value": 123}

        mock_collection.find_one.return_value = document
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.get_document(collection_name, query)

        mock_collection.find_one.assert_called_once_with(query)
        assert result["_id"] == str(document["_id"])
        assert result["name"] == document["name"]

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_document_with_id_query(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        document_id = str(ObjectId())
        query = {"id": document_id}
        document = {"_id": ObjectId(document_id), "name": "test"}

        mock_collection.find_one.return_value = document
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.get_document(collection_name, query)

        call_args = mock_collection.find_one.call_args[0][0]
        assert "_id" in call_args
        assert "id" not in call_args
        assert result["_id"] == str(document["_id"])

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_document_returns_none_when_not_found(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        query = {"name": "non_existent"}

        mock_collection.find_one.return_value = None
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.get_document(collection_name, query)

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_update_document_successfully(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        query = {"name": "test"}
        document = {"value": 456}
        updated_document = {"_id": ObjectId(), "name": "test", "value": 456}

        mock_collection.find_one.return_value = updated_document
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.update_document(collection_name, query, document)

        mock_collection.update_one.assert_called_once()
        assert result["_id"] == str(updated_document["_id"])
        assert result["value"] == updated_document["value"]

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_documents_successfully(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        query = {"status": "active"}
        documents = [
            {"_id": ObjectId(), "name": "doc1", "status": "active"},
            {"_id": ObjectId(), "name": "doc2", "status": "active"},
        ]

        class AsyncIterator:
            def __init__(self, items):
                self.items = items
                self.index = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.index >= len(self.items):
                    raise StopAsyncIteration
                item = self.items[self.index]
                self.index += 1
                return item

        mock_cursor = AsyncIterator(documents)
        mock_collection.find.return_value = mock_cursor
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.get_all_documents(collection_name, query)

        assert len(result) == 2
        assert all("_id" in doc and isinstance(doc["_id"], str) for doc in result)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_get_all_documents_with_empty_query(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        documents = [{"_id": ObjectId(), "name": "doc1"}]

        class AsyncIterator:
            def __init__(self, items):
                self.items = items
                self.index = 0

            def __aiter__(self):
                return self

            async def __anext__(self):
                if self.index >= len(self.items):
                    raise StopAsyncIteration
                item = self.items[self.index]
                self.index += 1
                return item

        mock_cursor = AsyncIterator(documents)
        mock_collection.find.return_value = mock_cursor
        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        result = await mongo_service.get_all_documents(collection_name)

        assert len(result) == 1
        assert result[0]["_id"] == str(documents[0]["_id"])

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_delete_document_successfully(
        self,
        mongo_service: MongoService,
        mock_collection: MagicMock,
        mocker: MockFixture,
    ):
        collection_name = "test_collection"
        query = {"name": "test"}

        mongo_service.db = MagicMock()
        mongo_service.db.__getitem__ = MagicMock(return_value=mock_collection)

        await mongo_service.delete_document(collection_name, query)

        mock_collection.delete_one.assert_called_once_with(query)
