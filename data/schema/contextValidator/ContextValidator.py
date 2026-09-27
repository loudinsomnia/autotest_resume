import decimal

from pydantic import BaseModel, model_validator, ValidationInfo, ValidationError
from typing import List
from pydantic_core import PydanticCustomError, InitErrorDetails
from typing import Any


class ContextValidatorModel(BaseModel):
    @model_validator(mode='after')
    def validate_context(self, info: ValidationInfo):
        # Если контекст не передан, пропускаем дополнительные проверки.
        if not info.context:
            return self
        # Имя текущей модели и ее объявленные поля.
        class_name = self.__class__.__name__
        fields = type(self).model_fields
        errors: List[InitErrorDetails] = []
        # Проходим по всем ожидаемым значениям из context.
        for key, expected_value in info.context.items():
            field_name = None
            # Поддержка формата ключа "<ClassName>_<field>".
            if key.startswith(f"{class_name}_"):
                field_name = key.replace(f"{class_name}_", "", 1)
            # Поддержка короткого формата "<field>".
            elif key in fields and f"{class_name}_{key}" not in info.context:
                field_name = key
            if field_name and field_name in fields:
                # Берем фактическое значение поля из модели.
                actual = getattr(self, field_name)
                # Для Decimal сравниваем через Decimal, чтобы избежать ошибок типов.
                if isinstance(actual, decimal.Decimal):
                    exp_decimal = decimal.Decimal(str(expected_value))
                    is_equal = actual.compare(exp_decimal) == 0
                else:
                    # Для остальных типов используем обычное сравнение.
                    is_equal = (actual == expected_value)
                # Падаем с понятным сообщением при несовпадении.
                if not is_equal:
                    errors.append(InitErrorDetails(type=PydanticCustomError(
                        'context_mismatch',
                        "Поле '{field}': ожидалось {expected}, получили {actual}",
                        {'field': field_name,
                         'expected': expected_value,
                         'actual': actual}
                    ), loc=(field_name,)))
        if errors:
            raise ValidationError.from_exception_data(
                title=class_name,
                line_errors=errors
            )
        return self
