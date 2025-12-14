from unittest.mock import MagicMock

import pytest
from pytest_mock import MockFixture

from modules.shared.services.redis.redis_service import RedisService


class TestRedisService:
    @pytest.fixture
    def redis_service(self) -> RedisService:
        return RedisService(connection_string="redis://localhost:6379")

    @pytest.fixture
    def mock_redis_client(self, mocker: MockFixture):
        mock_client = MagicMock()
        mock_client.ping = MagicMock()
        mock_client.get = MagicMock()
        mock_client.set = MagicMock()
        mock_client.setex = MagicMock()
        mock_client.delete = MagicMock()
        return mock_client

    @pytest.mark.unit
    def test_get_value_successfully(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        expected_value = "test_value"
        mock_redis_client.get.return_value = expected_value.encode("utf-8")

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.get_value(key)

        mock_redis_client.get.assert_called_once_with(key)
        assert result == expected_value

    @pytest.mark.unit
    def test_get_value_returns_default_when_key_not_found(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "non_existent_key"
        default_value = "default"
        mock_redis_client.get.return_value = None

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.get_value(key, default_value)

        mock_redis_client.get.assert_called_once_with(key)
        assert result == default_value

    @pytest.mark.unit
    def test_get_value_handles_string_value(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        expected_value = "string_value"
        mock_redis_client.get.return_value = expected_value

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.get_value(key)

        assert result == expected_value

    @pytest.mark.unit
    def test_get_value_returns_default_on_exception(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        default_value = "default"
        mock_redis_client.get.side_effect = Exception("Connection error")

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.get_value(key, default_value)

        assert result == default_value

    @pytest.mark.unit
    def test_set_value_successfully(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        value = "test_value"
        mock_redis_client.set.return_value = True

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.set_value(key, value)

        mock_redis_client.set.assert_called_once_with(key, value)
        assert result is True

    @pytest.mark.unit
    def test_set_value_with_expiration(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        value = "test_value"
        expire_in_milliseconds = 60000
        expire_seconds = 60

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.set_value(key, value, expire_in_milliseconds)

        mock_redis_client.setex.assert_called_once_with(key, expire_seconds, value)
        assert result is True

    @pytest.mark.unit
    def test_set_value_returns_false_when_client_is_none(
        self, redis_service: RedisService, mocker: MockFixture
    ):
        key = "test_key"
        value = "test_value"

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=None
        )

        result = redis_service.set_value(key, value)

        assert result is False

    @pytest.mark.unit
    def test_set_value_returns_false_on_exception(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        value = "test_value"
        mock_redis_client.set.side_effect = Exception("Connection error")

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.set_value(key, value)

        assert result is False

    @pytest.mark.unit
    def test_delete_value_successfully(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        mock_redis_client.delete.return_value = 1

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.delete_value(key)

        mock_redis_client.delete.assert_called_once_with(key)
        assert result is True

    @pytest.mark.unit
    def test_delete_value_returns_false_when_key_not_found(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "non_existent_key"
        mock_redis_client.delete.return_value = 0

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.delete_value(key)

        assert result is False

    @pytest.mark.unit
    def test_delete_value_returns_false_when_client_is_none(
        self, redis_service: RedisService, mocker: MockFixture
    ):
        key = "test_key"

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=None
        )

        result = redis_service.delete_value(key)

        assert result is False

    @pytest.mark.unit
    def test_delete_value_returns_false_on_exception(
        self,
        redis_service: RedisService,
        mock_redis_client: MagicMock,
        mocker: MockFixture,
    ):
        key = "test_key"
        mock_redis_client.delete.side_effect = Exception("Connection error")

        mocker.patch.object(
            redis_service, "_RedisService__get_client", return_value=mock_redis_client
        )

        result = redis_service.delete_value(key)

        assert result is False
