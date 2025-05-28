#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from typing import Any, List, Optional

from machine_tools import ListNameFormatter, MachineFormatter, SoftwareControl
from machine_tools.app.db.query_builder import QueryBuilder
from machine_tools.app.db.session_manager import Session, session_manager


class MachineFinderForOperations:
    """
    Кастомный поисковик для поиска имен станков по операциям.
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
        self,
        group: Optional[int] = None,
        subgroups: Optional[int] = None,
        software_control: SoftwareControl = SoftwareControl.NO,
    ) -> List[Any]:
        """Получение станков по группе, типу и типу управления"""
        self._builder.reset_builder()
        if group:
            self._builder.filter_by_group(group)
        if subgroups:
            self._builder.filter_by_type(subgroups)
        if software_control:
            self._builder.filter_by_software_control(software_control.value)
        machines = self._builder.execute()
        return self._formatter.format(machines)

    def get_cnc_names(
        self,
        group: Optional[int] = None,
        subgroups: Optional[int] = None,
    ) -> List[Any]:
        """Получение имен станков с ЧПУ, по группе и типу"""
        return self.get_names_by_condition(group, subgroups, SoftwareControl.CNC)

    def get_no_cnc_names(
        self,
        group: Optional[int] = None,
        subgroups: Optional[int] = None,
    ) -> List[Any]:
        """Получение имен станков без ЧПУ, по группе и типу"""
        names = []
        names.extend(self.get_names_by_condition(group, subgroups, SoftwareControl.NO))
        names.extend(self.get_names_by_condition(group, subgroups, SoftwareControl.IC))
        return names
