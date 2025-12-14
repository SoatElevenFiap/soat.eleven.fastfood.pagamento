CLIENT_BASE_CACHE = "client:"


class ClientCacheKeys:
    @staticmethod
    def client_key_for(client_id: str) -> str:
        return CLIENT_BASE_CACHE + client_id

    ALL_CLIENTS_KEY = CLIENT_BASE_CACHE + "all"
