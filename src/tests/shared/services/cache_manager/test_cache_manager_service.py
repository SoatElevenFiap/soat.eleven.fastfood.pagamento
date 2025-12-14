import json
from unittest.mock import MagicMock

import pytest
from pydantic import BaseModel
from pytest_mock import MockFixture

from modules.shared.adapters.cache_adapter import CacheAdapter
from modules.shared.services.cache_manager.cache_manager_service import (
    CacheManagerService,
)


class SampleModel(BaseModel):
    id: str
    name: str


class ConcreteCacheManagerService(CacheManagerService):
    pass


class TestCacheManagerService:
    @pytest.fixture
    def cache_adapter(self, mocker: MockFixture) -> CacheAdapter:
        mock_cache = MagicMock(spec=CacheAdapter)
        mock_cache.get_value = MagicMock()
        mock_cache.set_value = MagicMock(return_value=True)
        mock_cache.delete_value = MagicMock(return_value=True)
        return mock_cache

    @pytest.fixture
    def cache_manager_service(
        self, cache_adapter: CacheAdapter
    ) -> ConcreteCacheManagerService:
        return ConcreteCacheManagerService(cache=cache_adapter)

    @pytest.mark.unit
    def test_get_value_successfully(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        expected_value = "test_value"
        cache_adapter.get_value.return_value = expected_value

        result = cache_manager_service.get_value(key)

        cache_adapter.get_value.assert_called_once_with(key, None)
        assert result == expected_value

    @pytest.mark.unit
    def test_get_value_with_default(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        default_value = "default"
        cache_adapter.get_value.return_value = default_value

        result = cache_manager_service.get_value(key, default_value)

        cache_adapter.get_value.assert_called_once_with(key, default_value)
        assert result == default_value

    @pytest.mark.unit
    def test_set_value_with_string(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        value = "test_value"

        result = cache_manager_service.set_value(key, value)

        cache_adapter.set_value.assert_called_once_with(key, value, None)
        assert result is True

    @pytest.mark.unit
    def test_set_value_with_base_model(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        value = SampleModel(id="123", name="Test")
        expected_json = value.model_dump_json()

        result = cache_manager_service.set_value(key, value)

        cache_adapter.set_value.assert_called_once_with(key, expected_json, None)
        assert result is True

    @pytest.mark.unit
    def test_set_value_with_list_of_base_models(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        value = [SampleModel(id="1", name="Test1"), SampleModel(id="2", name="Test2")]
        expected_json = json.dumps(
            [item.model_dump(mode="json", by_alias=True) for item in value]
        )

        result = cache_manager_service.set_value(key, value)

        cache_adapter.set_value.assert_called_once_with(key, expected_json, None)
        assert result is True

    @pytest.mark.unit
    def test_set_value_with_empty_list(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        value = []
        expected_json = json.dumps([])

        result = cache_manager_service.set_value(key, value)

        cache_adapter.set_value.assert_called_once_with(key, expected_json, None)
        assert result is True

    @pytest.mark.unit
    def test_set_value_with_expiration(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        value = "test_value"
        expire_in_milliseconds = 60000

        result = cache_manager_service.set_value(key, value, expire_in_milliseconds)

        cache_adapter.set_value.assert_called_once_with(
            key, value, expire_in_milliseconds
        )
        assert result is True

    @pytest.mark.unit
    def test_expire_keys_successfully(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        keys = ["key1", "key2", "key3"]
        cache_adapter.delete_value.return_value = True

        result = cache_manager_service.expire_keys(keys)

        assert cache_adapter.delete_value.call_count == len(keys)
        assert result is True

    @pytest.mark.unit
    def test_expire_keys_returns_false_when_some_fail(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        keys = ["key1", "key2", "key3"]
        cache_adapter.delete_value.side_effect = [True, False, True]

        result = cache_manager_service.expire_keys(keys)

        assert result is False

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_build_cache_operation_returns_cached_value(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        cached_value = "cached_value"

        async def callback():
            return "new_value"

        cache_adapter.get_value.return_value = cached_value

        result = await cache_manager_service.build_cache_operation(key, callback)

        cache_adapter.get_value.assert_called_once_with(key, None)
        assert result == cached_value

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_build_cache_operation_calls_callback_when_no_cache(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        callback_value = "callback_value"

        async def callback():
            return callback_value

        cache_adapter.get_value.return_value = None

        result = await cache_manager_service.build_cache_operation(key, callback)

        cache_adapter.get_value.assert_called_once_with(key, None)
        cache_adapter.set_value.assert_called_once_with(key, callback_value, None)
        assert result == callback_value

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_build_cache_operation_with_entity_class(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        test_model = SampleModel(id="123", name="Test")
        cached_json = test_model.model_dump_json()

        async def callback():
            return test_model

        cache_adapter.get_value.return_value = cached_json

        result = await cache_manager_service.build_cache_operation(
            key, callback, entity_class=SampleModel
        )

        assert isinstance(result, SampleModel)
        assert result.id == test_model.id
        assert result.name == test_model.name

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_build_cache_operation_with_list_of_entities(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"
        test_models = [
            SampleModel(id="1", name="Test1"),
            SampleModel(id="2", name="Test2"),
        ]
        cached_json = json.dumps([item.model_dump() for item in test_models])

        async def callback():
            return test_models

        cache_adapter.get_value.return_value = cached_json

        result = await cache_manager_service.build_cache_operation(
            key, callback, entity_class=SampleModel
        )

        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(item, SampleModel) for item in result)

    @pytest.mark.asyncio
    @pytest.mark.unit
    async def test_build_cache_operation_does_not_cache_none(
        self,
        cache_manager_service: ConcreteCacheManagerService,
        cache_adapter: MagicMock,
    ):
        key = "test_key"

        async def callback():
            return None

        cache_adapter.get_value.return_value = None

        result = await cache_manager_service.build_cache_operation(key, callback)

        cache_adapter.set_value.assert_not_called()
        assert result is None
