from __future__ import annotations

from dataclasses import dataclass

from app.users import User, LocalUser, ForeignUser


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

    def register_call(self, raw_call: str) -> ActiveCall:
        '''
        Метод должен принимать только 1 строку и возвращать класс ActiveCall.
        На входе строка должна быть вида "caller_id,caller_name,caller_phone,reciever_id,reciever_name,reciever_phone"

        Например: "1001,Иван Петров,+71234567890,1085,Адам Яковлев,+71255556666"
        '''

        def create_user_by_phone(user_id: int, name: str, phone: str) -> User:

            if LOCAL_PHONE_PREFIX in phone:
                return LocalUser(user_id, name, phone)
            else:
                return ForeignUser(user_id, name, phone)

        parts = raw_call.split(',')

        if len(parts) != 6:
            raise ValueError(f"Ожидается 6 полей, получено {len(parts)}")

        caller_id, caller_name, caller_phone, receiver_id, receiver_name, receiver_phone = parts

        caller = create_user_by_phone(int(caller_id), caller_name, caller_phone)
        receiver = create_user_by_phone(int(receiver_id), receiver_name, receiver_phone)

        new_active_call = ActiveCall(caller, receiver)

        self._active_calls.append(new_active_call) # кладем в массив для подсчёта в следующей функции
        return new_active_call

    def get_active_calls_count(self) -> int:
        return len(self._active_calls)

    def get_cross_border_calls_count(self) -> int:
        count = 0
        for user in self._active_calls:
            if user.is_cross_border:
                count += 1
        return count