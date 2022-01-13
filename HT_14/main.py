from cash_machine_service import CashMachineService
from system import System
from system_dao import SystemDao
from user_service import UserService


def main() -> None:
    system_dao = SystemDao()
    user_service = UserService(system_dao)
    cash_machine_service = CashMachineService(system_dao, user_service)
    system = System(user_service, cash_machine_service)
    system.start()


main()



