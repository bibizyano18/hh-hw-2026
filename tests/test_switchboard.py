import pytest

from app.switchboard import Switchboard
from app.users import ForeignUser, LocalUser


def test_register_call_creates_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert active_call.caller.id == 1
    assert active_call.receiver.id == 2


def test_register_call_counts_active_calls() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )
    switchboard.register_call(
        "3,John Smith,+15551234567,4,Jane Doe,+33123456789"
    )

    assert switchboard.get_active_calls_count() == 2


def test_register_call_counts_calls_between_local_and_foreign_users() -> None:
    switchboard = Switchboard()

    switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    switchboard.register_call(
        "3,Petr Petrov,+78880000000,4,Maria Petrova,+79991112233"
    )
    switchboard.register_call(
        "5,Jane Doe,+33123456789,6,Alex Doe,+442012345678"
    )

    assert switchboard.get_active_calls_count() == 3
    assert switchboard.get_cross_border_calls_count() == 1

def test_register_call_with_local_to_local_calls() -> None:
    # тест для звонков между локальными пользователями"""
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,Petr Petrov,+78880000000"
    )

    assert isinstance(active_call.caller, LocalUser)
    assert isinstance(active_call.receiver, LocalUser)
    assert switchboard.get_cross_border_calls_count() == 0


def test_register_call_with_foreign_to_foreign_calls() -> None:
    # тест для звонков между иностранными пользователями
    switchboard = Switchboard()

    active_call = switchboard.register_call(
        "1,John Smith,+15551234567,2,Jane Doe,+33123456789"
    )

    assert isinstance(active_call.caller, ForeignUser)
    assert isinstance(active_call.receiver, ForeignUser)
    assert switchboard.get_cross_border_calls_count() == 0


def test_register_call_multiple_calls_with_same_users() -> None:
    # тест с несколькими звонками между одними и теми же пользователями
    switchboard = Switchboard()

    call1 = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )
    call2 = switchboard.register_call(
        "1,Ivan Ivanov,+79990000000,2,John Smith,+15551234567"
    )

    assert switchboard.get_active_calls_count() == 2
    assert call1 is not call2  # разные объекты
    assert call1.caller.id == call2.caller.id  # но одинаковые данные

