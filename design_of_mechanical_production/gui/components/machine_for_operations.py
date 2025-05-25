#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional

from machine_tools import ListNameFormatter, MachineFormatter, SoftwareControl
from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.db.session_manager import Session, session_manager

OPERATIONS_MAP = {
    "Токарная": (1, None, "NO_CNC"),
    "Токарная с ЧПУ": (1, None, "CNC"),
    "Расточная": (1, None, "NO_CNC"),
    "Расточная с ЧПУ": (1, None, "CNC"),
    "Сверлильная": (2, None, "NO_CNC"),
    "Сверлильная с ЧПУ": (2, None, "CNC"),
    "Фрезерная": (6, None, "NO_CNC"),
    "Фрезерная с ЧПУ": (6, None, "CNC"),
    "Шлифовальная": (3, None, "NO_CNC"),
    "Шлифовальная с ЧПУ": (3, None, "CNC"),
    "Протяжная": (7, None, "NO_CNC"),
    "Протяжная с ЧПУ": (7, None, "CNC"),
    "Строгальная": (7, None, "NO_CNC"),
    "Строгальная с ЧПУ": (7, None, "CNC"),
}


class MachineFinderForOperations:
    """
    Класс для поиска имен станков по операциям.
    """

    def __init__(
        self,
        session: Optional[Session] = None,
        formatter: Optional[MachineFormatter] = None,
    ):
        """
        Инициализация поисковика.

        Args:
            session (Session, optional): Сессия БД. Если не указана, будет создана новая.
            formatter (MachineFormatter, optional): Форматер для результатов. По умолчанию ListNameFormatter
        """
        self.session_manager = session_manager
        self.session: Session = session or self.session_manager.get_session()
        self._builder: QueryBuilder = QueryBuilder(self.session)
        self._formatter: MachineFormatter = formatter or ListNameFormatter()
        self.operation_map = OPERATIONS_MAP

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session_manager.close_session()

    def all(self) -> List[Any]:
        """Получение всех станков"""
        machines = self._builder.execute()
        return self._formatter.format(machines)

    def get_names_by_condition(
        self, group: int, type_: Optional[int] = None, software_control: SoftwareControl = SoftwareControl.NO
    ) -> List[Any]:
        """Получение станков по группе, типу и типу управления"""
        self._builder.reset_builder()
        self._builder.filter_by_group(group)
        if type_:
            self._builder.filter_by_type(type_)
        if software_control:
            self._builder.filter_by_software_control(software_control.value)
        machines = self._builder.execute()
        return self._formatter.format(machines)

    def get_cnc_names(
        self,
        group: int,
        type_: Optional[int] = None,
    ) -> List[Any]:
        """Получение имен станков с ЧПУ, по группе и типу"""
        return self.get_names_by_condition(group, type_, SoftwareControl.CNC)

    def get_no_cnc_names(
        self,
        group: int,
        type_: Optional[int] = None,
    ) -> List[Any]:
        """Получение имен станков без ЧПУ, по группе и типу"""
        names = []
        names.extend(self.get_names_by_condition(group, type_, SoftwareControl.NO))
        names.extend(self.get_names_by_condition(group, type_, SoftwareControl.IC))
        return names


class OperationMapFactory:
    def __init__(self):
        self.operation_map = OPERATIONS_MAP
        self.machine_finder = MachineFinderForOperations()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.machine_finder.session:
            self.machine_finder.session_manager.close_session()

    def get_map(self):
        """Получение словаря с операциями и доступными именами станков"""
        _names_map = {}
        for description, parameters in self.operation_map.items():
            if parameters[2] == "CNC":
                _names_map[description] = self.machine_finder.get_cnc_names(parameters[0], parameters[1])
            elif parameters[2] == "NO_CNC":
                _names_map[description] = self.machine_finder.get_no_cnc_names(parameters[0], parameters[1])
        return _names_map


if __name__ == "__main__":
    with OperationMapFactory() as find:
        # names = find.get_CNC_names(group=1)
        # print(names)
        # print(len(names))
        #
        # names = find.get_NO_CNC_names(group=1)
        # print(names)
        # print(len(names))

        names_map = find.get_map()
        for key, value in names_map.items():
            print(f"{key} ({len(value)}): {value}")
