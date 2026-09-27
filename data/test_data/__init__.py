import copy
import json
from pathlib import Path
from utils.base_meta import Singleton
from easydict import EasyDict
import logging


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)



class Reader(metaclass=Singleton):
    """
    Класс для работы с JSON-файлами.
    Он позволяет найти файл, прочитать его содержимое и обновить данные
    по пути, указанному в формате "ключ1.ключ2..." или "ключ1[].ключ2...".
    """

    def file_finder(self, file,folder=None):
        """Найти первый файл, соответствующий шаблону `file`."""
        if folder:
            f = Path('.').rglob(f"{folder}/**/{file}")
        else :
            f = Path('.').rglob(f"{file}")
        file_path = next((p for p in f), None)
        return file_path

    def read_data(self, file,folder=None):
        """
        Прочитать JSON-файл и вернуть его содержимое в виде EasyDict.
        """
        if folder:
            f_path = self.file_finder(file,folder)
        else:
            f_path = self.file_finder(file)
        with open(f_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return EasyDict(data)

    def update_data(self, data, update):
        """
        Обновить копию `data` согласно словарю `update`.
        Ключи в `update` могут содержать точку для вложенных структур.
        """
        obj = copy.deepcopy(data)
        if isinstance(obj, EasyDict):
            obj = dict(obj)
        for path, value in update.items():
            keys = path.split(".")
            self._changer(obj, keys, value)
        return obj

    def _changer(self, cur, keys, value):
        """
        Рекурсивно изменить структуру `cur` по списку `keys`.
        Поддерживается удаление (значение "DELETE") и обновление списков.
        """
        if not isinstance(cur, dict):
            return
        key = keys[0]
        # Обработка списка: ключ заканчивается на "[]"
        if key.endswith("[]"):
            list_key = key[:-2]
            for item in cur.get(list_key, []):
                self._changer(item, keys[1:], value)
            return
        # Если достигнут конец пути, применяем значение
        if len(keys) == 1:
            if value == "DELETE":
                cur.pop(key, None)
            else:
                cur[key] = value
            return

        # Переходим к следующему уровню вложенности
        next_value = cur.get(key)
        if next_value is None:
            cur[key] = {}
            next_value = cur[key]
        if not isinstance(next_value, dict):
            return
        self._changer(next_value, keys[1:], value)
