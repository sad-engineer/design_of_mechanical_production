#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from kivy.uix.screenmanager import Screen


class BaseWindow(Screen):
    """Базовый класс для всех окон приложения."""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = kwargs.get('name', 'base_window')
        
    def show(self) -> None:
        """Показывает окно."""
        if self.manager:
            self.manager.current = self.name
            
    def hide(self) -> None:
        """Скрывает окно."""
        if self.manager and self.manager.current == self.name:
            self.manager.current = 'main'
            
    def close(self) -> None:
        """Закрывает окно."""
        self.hide()
        
    def update(self, **kwargs) -> None:
        """Обновляет свойства окна."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                
    def refresh(self) -> None:
        """Обновляет все элементы окна."""
        self.canvas.ask_update()
        
    def is_closed(self) -> bool:
        """Проверяет, закрыто ли окно."""
        return self.manager is None or self.manager.current != self.name
        