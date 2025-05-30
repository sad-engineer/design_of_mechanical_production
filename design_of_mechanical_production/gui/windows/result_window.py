#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
"""
Модуль содержит класс окна отображения результатов расчета.
"""
from pathlib import Path

from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivy.uix.scrollview import ScrollView
from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.label import MDLabel

from design_of_mechanical_production.core import create_workshop_from_data
from design_of_mechanical_production.data.input import ExcelReader
from design_of_mechanical_production.data.output import TextReportGenerator
from design_of_mechanical_production.data.output.formatters import NumberFormatter
from design_of_mechanical_production.data.utils.file_system import (
    create_initial_data_file,
)
from design_of_mechanical_production.gui.components.notification_window import NotificationWindow
from design_of_mechanical_production.gui.windows.template_window import TemplateWindow
from design_of_mechanical_production.settings import get_setting

number_formatter = NumberFormatter()
fn = number_formatter.format


class TemplateResultWindow(TemplateWindow):
    """
    Окно отображения результатов расчета.

    Attributes:
        screen_manager: Менеджер экранов приложения
        workshop: Объект цеха с результатами расчета
    """

    def __init__(self, screen_manager=None, debug_mode=False, **kwargs):
        super().__init__(screen_manager=screen_manager, debug_mode=debug_mode, **kwargs)
        self.app = MDApp.get_running_app()
        self.label.text = "Расчетные данные"
        self.screen_manager = screen_manager
        self._workshop = None

        # создаем уведомление для экспорта
        self.export_notification = NotificationWindow(
            title="Экспорт",
            text="",
            button1_text="К расчету",
            button2_text="Выход",
            button1_callback=self.back_to_input,
            button2_callback=self.cancel,
        )
        # создаем контент
        self._create_content()
        # Инициализируем кнопки
        self._init_buttons()

    def _create_content(self):
        """Создает основной контент с результатами."""
        # Создаем ScrollView для прокрутки контента
        scroll_view = ScrollView(
            size_hint=(1, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            do_scroll_x=False,
        )

        # Создаем горизонтальный контейнер для двух колонок
        columns_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            spacing=10,
        )
        columns_layout.bind(minimum_height=columns_layout.setter('height'))

        # Создаем две вертикальные колонки
        self.left_column = BoxLayout(
            orientation='vertical',
            size_hint_x=0.4,
            size_hint_y=None,
            spacing=10,
            pos_hint={'top': 1},  # Привязываем к верху
        )
        self.right_column = BoxLayout(
            orientation='vertical',
            size_hint_x=0.6,
            size_hint_y=None,
            spacing=10,
            pos_hint={'top': 1},  # Привязываем к верху
        )

        # Привязываем высоту колонок к их содержимому
        self.left_column.bind(minimum_height=self.left_column.setter('height'))
        self.right_column.bind(minimum_height=self.right_column.setter('height'))

        # Добавляем колонки в горизонтальный контейнер
        columns_layout.add_widget(self.left_column)
        columns_layout.add_widget(self.right_column)

        # Добавляем горизонтальный контейнер в ScrollView
        scroll_view.add_widget(columns_layout)
        self.content.add_widget(scroll_view)

    def _init_buttons(self):
        """Инициализирует кнопки управления."""
        # Очищаем существующие кнопки
        self.buttons_box.clear_widgets()

        # Создаем новые кнопки
        back_to_input = Button(
            text='Назад', size_hint=(None, 1), width=self.max_button_width, on_release=self.back_to_input
        )
        export_results = Button(
            text='Экспорт', size_hint=(None, 1), width=self.max_button_width, on_release=self._on_export
        )
        # Добавляем кнопки в контейнер
        self.buttons_box.add_widget(back_to_input)
        self.buttons_box.add_widget(export_results)

    def back_to_input(self, instance):
        """
        Возвращает к окну ввода данных.
        """
        if self.screen_manager:
            self._workshop = None
            self.content.clear_widgets()
            self.screen_manager.current = 'input_window'

    def _on_export(self, instance):
        """
        Обрабатывает событие экспорта результатов.
        """
        report_path = self.export_results()
        if report_path:
            self.export_notification.text = f"Отчет успешно сгенерирован и сохранен в:\n{report_path}"
            self.export_notification.show()
        else:
            self.export_notification.text = "Ошибка при сохранении отчета"
            self.export_notification.show()

    def export_results(self):
        """
        Экспортирует результаты расчета в текстовый отчет.
        """
        if not self.workshop:
            print("Нет данных для экспорта")
            return
        # Генерация и сохранение отчета
        report_generator = TextReportGenerator()
        report = report_generator.generate_report(self.workshop)
        report_path = Path(get_setting('report_path'))
        result = report_generator.save_report(report, report_path)
        return report_path if result else None

    def _update_content_debug(self, instance, value):
        if self.debug_mode:
            instance.canvas.before.clear()
            with instance.canvas.before:
                Color(1, 1, 1, 0.5)  # белый с прозрачностью
                Rectangle(pos=instance.pos, size=instance.size)

    @property
    def workshop(self):
        return self._workshop

    @workshop.setter
    def workshop(self, workshop):
        """
        Устанавливает объект цеха и обновляет отображение.

        Args:
            workshop: Объект цеха с результатами расчета.
        """
        self._workshop = workshop
        if self._workshop:
            self.content.clear_widgets()
            self._create_content()
            self._update_content()

    @staticmethod
    def cancel(instance):
        """
        Отменяет ввод данных и завершает работу приложения.

        Args:
            instance: Экземпляр кнопки
        """
        # Завершаем работу приложения
        MDApp.get_running_app().stop()

    def _update_content(self):
        """Обновляет отображение результатов расчета."""
        # Левая колонка
        self.left_column.add_widget(self._add_general_info_card())
        self.left_column.add_widget(self._add_summary_card())
        self.left_column.add_widget(self._add_special_zones_equipment_card())
        self.left_column.add_widget(self._add_zones_info_card())

        # Правая колонка
        self.right_column.add_widget(self._add_process_info_card())
        self.right_column.add_widget(self._add_equipment_stats_card())
        self.right_column.add_widget(self._add_operations_stats_card())

    def _add_general_info_card(self):
        """Добавляет карточку с общей информацией о цехе."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=150,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Исходные данные',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация
        info_layout = BoxLayout(orientation='vertical', spacing=5)
        info_layout.add_widget(MDLabel(text=f'Название цеха: {self.workshop.name}'))
        info_layout.add_widget(MDLabel(text=f'Годовой объем производства: {fn(self.workshop.production_volume)} шт.'))
        info_layout.add_widget(MDLabel(text=f'Масса детали: {fn(self.workshop.mass_detail)} кг'))

        card.add_widget(info_layout)
        return card

    def _add_process_info_card(self):
        """Добавляет карточку с информацией о технологическом процессе в виде таблицы."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Технологический процесс\n(в пересчете на годовой объем)\n',
                font_style='H6',
                size_hint_y=None,
                size_hint_x=None,
                height=30,
                width=450,
                halign='center',
            )
        )

        # Таблица
        table = GridLayout(
            cols=3,
            size_hint_x=None,
            size_hint_y=None,
            row_default_height=25,
            spacing=5,
            padding=[0, 0, 0, 0],
        )
        table.width = 450
        table.cols_minimum = {0: table.width * 0.4, 1: table.width * 0.2, 2: table.width * 0.4}
        table.bind(minimum_height=table.setter('height'))

        # Заголовки таблицы
        headers = ['№/Название', 'Время, мин.', 'Станок']
        for header in headers:
            table.add_widget(MDLabel(text=header, bold=True, halign='center'))

        # Данные по операциям
        height = 150
        for operation in self.workshop.process.operations:
            table.add_widget(MDLabel(text=f"{str(operation.number)} {operation.name}", halign='left'))
            table.add_widget(MDLabel(text=str(fn(operation.time)), halign='center'))
            table.add_widget(MDLabel(text=operation.equipment.model, halign='center'))
            height += table.row_default_height + table.spacing[1]

        # Добавляем строку с общей трудоемкостью
        table.add_widget(MDLabel(text="Итого:  ", halign='right', bold=True))
        table.add_widget(MDLabel(text=str(fn(self.workshop.process.total_time)), halign='center', bold=True))
        table.add_widget(MDLabel(text="-", halign='center'))

        card.add_widget(table)
        card.height = height

        return card

    def _add_operations_stats_card(self):
        """Добавляет карточку с таблицей по операциям."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=325,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Анализ операций',
                font_style='H6',
                size_hint_y=None,
                size_hint_x=None,
                height=30,
                width=450,
                halign='center',
            )
        )

        # Таблица
        table = GridLayout(
            cols=4, size_hint_x=None, size_hint_y=None, row_default_height=25, spacing=5, padding=[0, 0, 0, 0]
        )
        table.width = 450
        table.cols_minimum = {
            0: table.width * 0.55,
            1: table.width * 0.15,
            2: table.width * 0.15,
            3: table.width * 0.15,
        }
        table.bind(minimum_height=table.setter('height'))

        headers = ['№/Название', 'Доля, %', 'Kv', 'Kp']
        for header in headers:
            table.add_widget(MDLabel(text=header, font_style='Subtitle2', halign='center'))

        height = 110
        for operation in self.workshop.process.operations:
            table.add_widget(MDLabel(text=f"{str(operation.number)} {operation.name}", halign='left'))
            table.add_widget(MDLabel(text=str(fn(operation.percentage)), halign='center'))
            table.add_widget(MDLabel(text=str(fn(operation.compliance_coefficient)), halign='center'))
            table.add_widget(MDLabel(text=str(fn(operation.progressivity_coefficient)), halign='center'))
            height += table.row_default_height + table.spacing[1]

        card.add_widget(table)
        card.height = height

        return card

    def _add_equipment_stats_card(self):
        """Добавляет карточку с таблицей по оборудованию."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=375,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Необходимое количество станков\nи их загрузка',
                font_style='H6',
                size_hint_y=None,
                size_hint_x=None,
                height=30,
                width=450,
                halign='center',
            )
        )
        table = GridLayout(
            cols=4, size_hint_x=None, size_hint_y=None, row_default_height=25, spacing=5, padding=[0, 0, 0, 0]
        )
        table.width = 450
        table.cols_minimum = {
            0: table.width * 0.55,
            1: table.width * 0.15,
            2: table.width * 0.15,
            3: table.width * 0.15,
        }
        table.bind(minimum_height=table.setter('height'))

        headers = ['№/Название', 'Nрасч', 'Nприн', 'Kзагр']
        for header in headers:
            table.add_widget(MDLabel(text=header, font_style='Subtitle2', halign='center'))

        height = 125
        for operation in self.workshop.process.operations:
            n_calc = getattr(operation, 'calculated_equipment_count', 0)
            n_accepted = getattr(operation, 'accepted_equipment_count', 0)
            load_coeff = getattr(operation, '_load_factor', 0)
            table.add_widget(MDLabel(text=f"{str(operation.number)} {operation.name}", halign='left'))
            table.add_widget(MDLabel(text=str(fn(n_calc)), halign='center'))
            table.add_widget(MDLabel(text=str(n_accepted), halign='center'))
            table.add_widget(MDLabel(text=str(fn(load_coeff)), halign='center'))
            height += table.row_default_height + table.spacing[1]

        # Добавляем строку итоговых значений
        table.add_widget(MDLabel(text="Итого:  ", halign='right', bold=True))
        table.add_widget(
            MDLabel(text=str(fn(self.workshop.process.calculated_machines_count)), halign='center', bold=True)
        )
        table.add_widget(MDLabel(text=str(self.workshop.process.accepted_machines_count), halign='center', bold=True))
        table.add_widget(MDLabel(text=str(fn(self.workshop.process.average_load_factor)), halign='center', bold=True))
        height += table.row_default_height + table.spacing[1]

        card.add_widget(table)
        card.height = height
        return card

    def _add_special_zones_equipment_card(self):
        """Добавляет карточку с информацией о специальных зонах."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=400,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        card.add_widget(
            MDLabel(
                text='Общее количество станков\nпо зонам',
                font_style='H6',
                size_hint_y=None,
                size_hint_x=None,
                height=30,
                width=450,
            )
        )

        grinding = self.workshop.zones.get('grinding_zone')
        repair = self.workshop.zones.get('repair_zone')
        main = self.workshop.zones.get('main_zone')
        total = self.workshop.total_machines_count

        # Информация
        card_layout = BoxLayout(orientation='vertical', spacing=5)

        card_layout.add_widget(MDLabel(text="Производственная зона:", halign='left'))
        card_layout.add_widget(
            MDLabel(text=f"    расчетное - {str(fn(main.calculated_machines_count))}", halign='left')
        )
        card_layout.add_widget(MDLabel(text=f"    принятое - {str(main.accepted_machines_count)}", halign='left'))

        card_layout.add_widget(MDLabel(text="Заточная зона:", halign='left'))
        card_layout.add_widget(
            MDLabel(text=f"    расчетное - {str(fn(grinding.calculated_machines_count))}", halign='left')
        )
        card_layout.add_widget(MDLabel(text=f"    принятое - {str(grinding.accepted_machines_count)}", halign='left'))

        card_layout.add_widget(MDLabel(text="Ремонтная зона:", halign='left'))
        card_layout.add_widget(
            MDLabel(text=f"    расчетное - {str(fn(repair.calculated_machines_count))}", halign='left')
        )
        card_layout.add_widget(MDLabel(text=f"    принятое - {str(repair.accepted_machines_count)}", halign='left'))

        card_layout.add_widget(MDLabel(text=f'Общее количество станков: {str(total)}', halign='left'))

        card.add_widget(card_layout)

        return card

    def _add_zones_info_card(self):
        """Добавляет карточку с информацией о зонах цеха."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=350,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )

        # Заголовок
        card.add_widget(
            MDLabel(
                text='Зоны цеха',
                font_style='H6',
                size_hint_y=None,
                height=30,
            )
        )

        # Информация о зонах
        zones_layout = BoxLayout(orientation='vertical', spacing=5)
        for zone_name, zone in self.workshop.zones.items():
            zones_layout.add_widget(
                MDLabel(
                    text=f'{zone.name}: {zone.area:.2f} м²',
                    size_hint_y=None,
                    height=25,
                )
            )

        zones_layout.add_widget(
            MDLabel(
                text=f"Расчетная площадь цеха: {fn(self.workshop.required_area)} м²",
                halign='left',
                height=25,
                bold=True,
            )
        )

        card.add_widget(zones_layout)
        return card

    def _add_summary_card(self):
        """Добавляет карточку с итоговыми значениями."""
        card = MDCard(
            orientation='vertical',
            size_hint=(1, None),
            height=180,
            padding=15,
            spacing=10,
            pos_hint={'top': 1},
            md_bg_color=self.app.theme_cls.disabled_primary_color,
        )
        card.add_widget(
            MDLabel(
                text='Итоговые значения',
                font_style='H6',
                size_hint_y=None,
                size_hint_x=None,
                height=30,
                width=450,
            )
        )

        # Добавляем строки
        card.add_widget(MDLabel(text=f"Ширина пролета: {fn(self.workshop.span_width)} м", halign='left'))
        card.add_widget(MDLabel(text=f"Число пролетов: {self.workshop.span_number}", halign='left'))
        card.add_widget(MDLabel(text=f"Общая ширина цеха: {fn(self.workshop.width)} м", halign='left'))
        card.add_widget(MDLabel(text=f"Длина цеха: {fn(self.workshop.length)} м", halign='left'))
        card.add_widget(MDLabel(text=f"Площадь цеха: {fn(self.workshop.total_area)} м²", halign='left', bold=True))
        return card


class ResultWindow(Screen):
    """Окно ввода данных, обертка для TemplateInputWindow."""

    def __init__(self, screen_manager=None, workshop=None, debug_mode=False, **kwargs):
        super().__init__(**kwargs)
        self.name = 'result_window'
        # Создаем и добавляем TemplateInputWindow
        self.template_window = TemplateResultWindow(screen_manager=screen_manager, debug_mode=debug_mode)
        self.template_window.workshop = workshop
        self.add_widget(self.template_window)

    @property
    def workshop(self):
        return self.template_window.workshop

    def set_workshop(self, workshop):
        """
        Устанавливает объект цеха и обновляет отображение.

        Args:
            workshop: Объект цеха с результатами расчета.
        """
        self.template_window.workshop = workshop


if __name__ == '__main__':

    class TestApp(MDApp):
        """Тестовое приложение для отладки окна."""

        def build(self):
            """Создает и возвращает главное окно приложения."""
            initial_data_file = create_initial_data_file()
            reader = ExcelReader(initial_data_file)
            parameters_data = reader.read_parameters_data()
            process_data = reader.read_process_data()
            workshop = create_workshop_from_data(parameters_data, process_data)

            Window.minimum_width = 910
            Window.minimum_height = 500
            window = ResultWindow(workshop=workshop, debug_mode=True)
            return window

    TestApp().run()
