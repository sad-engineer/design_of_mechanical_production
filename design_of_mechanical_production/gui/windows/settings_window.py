#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen

from design_of_mechanical_production.settings import get_setting, set_setting


class SettingsInput(BoxLayout):
    """Виджет для ввода настроек."""

    label_text = StringProperty()
    input_value = StringProperty()

    def __init__(self, label_text: str, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 40
        self.spacing = 10
        self.padding = [10, 5]
        self.size_hint_x = 0.8
        self.pos_hint = {'center_x': 0.5}

        # Получаем экземпляр приложения для доступа к теме
        self.app = MDApp.get_running_app()

        self.label = MDLabel(text=label_text, size_hint_x=0.55, halign='right', valign='middle', text_size=(None, None))
        self.label.bind(size=self._update_text_size)

        self.input = TextInput(
            text=self.input_value,
            size_hint_x=None,
            width=60,
            multiline=False,
            font_size=14,
            padding_x=5,
            input_filter='float',
            halign='center',
            background_color=self.app.theme_cls.bg_normal,
        )
        self.suf_label = MDLabel(text="", size_hint_x=0.15, halign='left', valign='middle', text_size=(None, None))
        self.suf_label.bind(size=self._update_text_size)

        self.add_widget(self.label)
        self.add_widget(self.input)
        self.add_widget(self.suf_label)

    @staticmethod
    def _update_text_size(instance, value):
        """Обновляет text_size метки при изменении её размера."""
        instance.text_size = (instance.width, instance.height)


class SettingsWindow(Screen):
    """Окно настроек приложения."""

    def __init__(self, previous_screen='input_window', **kwargs):
        super().__init__(**kwargs)
        self.name = 'settings'
        self.app = MDApp.get_running_app()
        self.previous_screen = previous_screen
        self._create_layout()

    def _create_layout(self) -> None:
        """Создает макет окна настроек."""
        # Основной контейнер
        main_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)

        # Заголовок
        title = MDLabel(
            text="Настройки расчета", size_hint_y=None, height=50, font_size=24, halign='center', font_style='H5'
        )
        main_layout.add_widget(title)

        # Создаем ScrollView
        scroll_view = ScrollView(size_hint=(1, 1), do_scroll_x=False, do_scroll_y=True)

        # Контейнер для прокручиваемого содержимого
        content_layout = BoxLayout(
            orientation='vertical', spacing=10, padding=10, size_hint_y=None, size_hint_x=1, pos_hint={'center_x': 0.5},
        )
        content_layout.bind(minimum_height=content_layout.setter('height'))

        # Фонд рабочего времени
        self.fund_of_working = SettingsInput("Фонд рабочего времени:")
        self.fund_of_working.input.text = str(get_setting("fund_of_working"))
        self.fund_of_working.suf_label.text = "часов"
        content_layout.add_widget(self.fund_of_working)

        # Коэффициенты
        self.kv = SettingsInput("Коэффициент выполнения норм:")
        self.kv.input.text = str(get_setting("kv"))
        content_layout.add_widget(self.kv)

        self.kp = SettingsInput("Коэффициент прогрессивности технологии:")
        self.kp.input.text = str(get_setting("kp"))
        content_layout.add_widget(self.kp)

        # Удельные площади
        self.tool_storage = SettingsInput("Склад инструмента:")
        self.tool_storage.input.text = str(get_setting("specific_areas.tool_storage"))
        self.tool_storage.suf_label.text = "м²"
        content_layout.add_widget(self.tool_storage)

        self.equipment_warehouse = SettingsInput("Склад приспособлений:")
        self.equipment_warehouse.input.text = str(get_setting("specific_areas.equipment_warehouse"))
        self.equipment_warehouse.suf_label.text = "м²"
        content_layout.add_widget(self.equipment_warehouse)

        self.work_piece_storage = SettingsInput("Склад заготовок и деталей:")
        self.work_piece_storage.input.text = str(get_setting("specific_areas.work_piece_storage"))
        self.work_piece_storage.suf_label.text = "м²"
        content_layout.add_widget(self.work_piece_storage)

        self.control_department = SettingsInput("Контрольное отделение:")
        self.control_department.input.text = str(get_setting("specific_areas.control_department"))
        self.control_department.suf_label.text = "м²"
        content_layout.add_widget(self.control_department)

        self.sanitary_zone = SettingsInput("Санитарно-бытовые помещения:")
        self.sanitary_zone.input.text = str(get_setting("specific_areas.sanitary_zone"))
        self.sanitary_zone.suf_label.text = "м²"
        content_layout.add_widget(self.sanitary_zone)

        # Проценты для зон
        self.grinding_zone = SettingsInput("Процент для заточного отделения:")
        self.grinding_zone.input.text = str(get_setting("grinding_zone_percent"))
        content_layout.add_widget(self.grinding_zone)

        self.repair_zone = SettingsInput("Процент для ремонтного отделения:")
        self.repair_zone.input.text = str(get_setting("repair_zone_percent"))
        content_layout.add_widget(self.repair_zone)

        # Площадь проходов
        self.passage_area = SettingsInput("Площадь проходов:")
        self.passage_area.input.text = str(get_setting("passage_area"))
        self.passage_area.suf_label.text = "м²"

        content_layout.add_widget(self.passage_area)

        # Настройки цеха
        self.workshop_span = SettingsInput("Ширина пролета цеха:")
        self.workshop_span.input.text = str(get_setting("workshop_span"))
        self.workshop_span.suf_label.text = "м"
        content_layout.add_widget(self.workshop_span)

        self.workshop_nam = SettingsInput("Количество пролетов:")
        self.workshop_nam.input.text = str(get_setting("workshop_nam"))
        content_layout.add_widget(self.workshop_nam)

        # Добавляем ScrollView в основной макет
        scroll_view.add_widget(content_layout)
        main_layout.add_widget(scroll_view)

        # Кнопки
        buttons = BoxLayout(size_hint_y=None, height=50, spacing=10)
        save_button = Button(
            text="Сохранить",
        )
        save_button.bind(on_press=self._save_settings)

        cancel_button = Button(
            text="Отмена",
        )
        cancel_button.bind(on_press=lambda x: self.hide())

        buttons.add_widget(save_button)
        buttons.add_widget(cancel_button)
        main_layout.add_widget(buttons)

        self.add_widget(main_layout)

    def _save_settings(self, instance) -> None:
        """Сохраняет настройки из полей ввода."""
        try:
            # Фонд рабочего времени
            new_fund = str(self.fund_of_working.input.text)
            if new_fund != str(get_setting("fund_of_working")):
                set_setting("fund_of_working", new_fund)

            # Коэффициенты
            new_kv = str(self.kv.input.text)
            if new_kv != str(get_setting("kv")):
                set_setting("kv", new_kv)

            new_kp = str(self.kp.input.text)
            if new_kp != str(get_setting("kp")):
                set_setting("kp", new_kp)

            # Удельные площади
            new_tool_storage = str(self.tool_storage.input.text)
            if new_tool_storage != str(get_setting("specific_areas.tool_storage")):
                set_setting("specific_areas.tool_storage", new_tool_storage)

            new_equipment_warehouse = str(self.equipment_warehouse.input.text)
            if new_equipment_warehouse != str(get_setting("specific_areas.equipment_warehouse")):
                set_setting("specific_areas.equipment_warehouse", new_equipment_warehouse)

            new_work_piece_storage = str(self.work_piece_storage.input.text)
            if new_work_piece_storage != str(get_setting("specific_areas.work_piece_storage")):
                set_setting("specific_areas.work_piece_storage", new_work_piece_storage)

            new_control_department = str(self.control_department.input.text)
            if new_control_department != str(get_setting("specific_areas.control_department")):
                set_setting("specific_areas.control_department", new_control_department)

            new_sanitary_zone = str(self.sanitary_zone.input.text)
            if new_sanitary_zone != str(get_setting("specific_areas.sanitary_zone")):
                set_setting("specific_areas.sanitary_zone", new_sanitary_zone)

            # Проценты для зон
            new_grinding_zone = str(self.grinding_zone.input.text)
            if new_grinding_zone != str(get_setting("grinding_zone_percent")):
                set_setting("grinding_zone_percent", new_grinding_zone)

            new_repair_zone = str(self.repair_zone.input.text)
            if new_repair_zone != str(get_setting("repair_zone_percent")):
                set_setting("repair_zone_percent", new_repair_zone)

            # Площадь проходов
            new_passage_area = str(self.passage_area.input.text)
            if new_passage_area != str(get_setting("passage_area")):
                set_setting("passage_area", new_passage_area)

            # Настройки цеха
            new_workshop_span = str(self.workshop_span.input.text)
            if new_workshop_span != str(get_setting("workshop_span")):
                set_setting("workshop_span", new_workshop_span)

            new_workshop_nam = str(self.workshop_nam.input.text)
            if new_workshop_nam != str(get_setting("workshop_nam")):
                set_setting("workshop_nam", new_workshop_nam)

            self.hide()
        except ValueError as e:
            print(f"Ошибка при сохранении настроек: {e}")
            # Здесь можно добавить всплывающее окно с ошибкой

    def hide(self):
        """Закрывает окно настроек и возвращается на предыдущий экран."""
        self.manager.transition.direction = 'right'
        self.manager.current = self.previous_screen


if __name__ == "__main__":
    from kivymd.app import MDApp

    class TestApp(MDApp):
        def build(self):
            return SettingsWindow()

    TestApp().run()
