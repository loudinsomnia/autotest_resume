import grpc
import logging
from typing import Any, Type, Optional
from utils.base_meta import Singleton

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("GRPCClient")


class GRPCClient(metaclass=Singleton):
    def __init__(self, host, port, sec, stubs, cred_path):
        self.target = f"{host}:{port}"
        self.secure = sec
        self.credentials_path = cred_path
        self.stubs_classes = stubs
        self._channel: Optional[grpc.Channel] = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close

    def connect(self) -> grpc.Channel:
        if self._channel is not None:
            return self._channel
        if self.secure:
            if self.credentials_path:
                with open(self.credentials_path, 'rb') as f:
                    cred = grpc.ssl_channel_credentials(f.read())
            else:
                cred = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel(self.target, cred)
            logger.info(f"Установлено безопасное TLS соединение с {self.target}")
        else:
            self._channel = grpc.insecure_channel(self.target)
            logger.info(f"Установлено незащищенное соединение с {self.target}")
        for stub_cls in self.stubs_classes:
            # Превращает 'QuotesStreamServiceStub' в строку 'quotesstreamservice'
            friendly_name = stub_cls.__name__.replace('Stub', '').lower()
            # Регистрируем инициализированный стаб как атрибут класса
            setattr(self, friendly_name, stub_cls(self._channel))
        return self._channel

    def call(self, stub_class: Type, method_name: str, request_message: Any):
        if not self._channel:
            raise RuntimeError(
                "Канал не инициализирован. Вызовите метод connect() или используйте контекстный менеджер.")
        stub = stub_class(self._channel)
        try:
            grpc_method = getattr(stub, method_name)
        except AttributeError:
            raise AttributeError(f"Метод '{method_name}' не найден в заглушке {stub_class.__name__}")
        try:
            logger.info(f"Отправка RPC запроса {method_name}...")
            response = grpc_method(request_message)
            return response
        except grpc.RpcError as e:
            logger.error(f"Ошибка gRPC при вызове {method_name}: {e.code()} - {e.details()}")
            raise e

    def close(self):
        if self._channel:
            self._channel.close()
            self._channel = None
            logger.info(f"Канал соединения с {self.target} закрыт")
