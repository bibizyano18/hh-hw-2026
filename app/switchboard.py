from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser
from typing import Tuple


LOCAL_PHONE_PREFIX = "+7"


@dataclass(slots=True)
class ActiveCall:
    caller: User
    receiver: User

    @property
    def is_cross_border(self) -> bool:
        return type(self.caller) is not type(self.receiver)


class Switchboard:
    def __init__(self) -> None:
        self._active_calls: list[ActiveCall] = []
        self._cross_border_calls: list[ActiveCall] = []

    # возвращает кортеж с проверенными данными
    @staticmethod
    def validate_and_parse_call_data(raw_call: str) -> Tuple[int, str, str, int, str, str]:
        parts = raw_call.split(',')

        if len(parts) != 6:
            raise ValueError(f"Ожидается 6 полей, получено {len(parts)}")

        caller_id_str, caller_name, caller_phone, receiver_id_str, receiver_name, receiver_phone = parts

        if not caller_id_str.isdigit():
            raise ValueError(f"caller_id должен быть числом, получено: {caller_id_str}")
        if not receiver_id_str.isdigit():
            raise ValueError(f"receiver_id должен быть числом, получено: {receiver_id_str}")
        caller_id = int(caller_id_str)
        receiver_id = int(receiver_id_str)
        if caller_id <= 0 or receiver_id <= 0:
            raise ValueError("ID пользователей должны быть положительными числами")

        if not caller_name:
            raise ValueError("caller_name не может быть пустым")
        if not receiver_name:
            raise ValueError("receiver_name не может быть пустым")

        def validate_phone(phone: str, field_name: str) -> None:
            if not phone:
                raise ValueError(f"{field_name} не может быть пустым")
            if not phone.startswith('+'):
                raise ValueError(f"{field_name} должен начинаться с '+', получено: {phone}")
            # проверяем, что после + только цифры
            if not phone[1:].isdigit():
                raise ValueError(f"{field_name} должен содержать только цифры после '+', получено: {phone}")

        validate_phone(caller_phone, "caller_phone")
        validate_phone(receiver_phone, "receiver_phone")

        return caller_id, caller_name, caller_phone, receiver_id, receiver_name, receiver_phone

    @staticmethod
    def create_user_by_phone(user_id: int, name: str, phone: str) -> User:

        if phone.startswith(LOCAL_PHONE_PREFIX):
            return LocalUser(user_id, name, phone)
        else:
            return ForeignUser(user_id, name, phone)

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''
        (caller_id, caller_name, caller_phone,
         receiver_id, receiver_name, receiver_phone) = self.validate_and_parse_call_data(raw_call)
        caller = self.create_user_by_phone(int(caller_id), caller_name, caller_phone)
        receiver = self.create_user_by_phone(int(receiver_id), receiver_name, receiver_phone)

        new_active_call = ActiveCall(caller, receiver)

        self._active_calls.append(new_active_call) # кладем в массив для подсчёта в следующей функции
        if new_active_call.is_cross_border: # оптимизируем функцию get_cross_border, кладем звонок в массив на этапе создания звонка
            self._cross_border_calls.append(new_active_call)
        return new_active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        return len(self._cross_border_calls)