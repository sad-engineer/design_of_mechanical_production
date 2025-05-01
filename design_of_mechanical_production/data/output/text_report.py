#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
from decimal import Decimal
from pathlib import Path
from typing import List

from design_of_mechanical_production.core.entities.workshop import Workshop
from design_of_mechanical_production.core.interfaces.formatters import INumberFormatter, ITableFormatter
from design_of_mechanical_production.core.interfaces.report_generator import IReportGenerator
from design_of_mechanical_production.data.output.formatters import NumberFormatter, TableFormatter
from design_of_mechanical_production.settings import get_setting


class TextReportGenerator(IReportGenerator):
    """
    Класс для генерации текстовых отчетов.
    """

    def __init__(self, number_formatter: INumberFormatter = None, table_formatter: ITableFormatter = None):
        self.number_formatter = number_formatter or NumberFormatter()
        self.table_formatter = table_formatter or TableFormatter()

    def generate_report(self, workshop: Workshop) -> str:
        """
        Генерирует текстовый отчет о цехе.
        """
        report = list()
        report.append(f"Отчет по цеху: {workshop.name}")

        report.append(f"1. Исходные данные:")
        report.append("")
        report_total_time = self.number_formatter.format(workshop.process.total_time)
        report.append(f"Трудоемкость изготовления 1 тонны изделия − {report_total_time} нормо-часа.")
        report.append(f"Годовой объем выпуска продукции – {workshop.production_volume} шт.")
        report.append(f"Трудоемкость производственной программы по операциям определяется по формуле:")

        report.append(f"Т_ОП = t_g∙ N ∙ П_ОП")
        report.append(f"где t_g –  трудоёмкость детале-операции, ч.;")
        report.append(f"t_g = {report_total_time} н-ч.;")
        report.append(f"N – годовой объём выпуска;")
        report.append(f"N = {workshop.production_volume} шт.;")
        report.append(f"П_ОП – процентное содержание операции, %.")
        report.append("")

        report.append(f"Таблица 1 - Наименование операций")

        # Подготавливаем данные для таблицы
        headers = ["№ операции", "Наименование операции", "Доля от общей трудоемкости", "T_штi,н-ч"]
        table_data = []
        for operation in workshop.process.operations:
            percentage = f"{self.number_formatter.format(operation.percentage)}%"
            time = self.number_formatter.format(operation.time * Decimal(str(workshop.production_volume)))
            number = f"{operation.number}"
            table_data.append((number, operation.name, percentage, time))
        # Строка итога
        total_row = ('', '', 'Итого', report_total_time)
        # Форматируем таблицу
        report.extend(self.table_formatter.format(headers, table_data, total_row))

        report.append("")

        report.append("2. Расчётное количество станков на каждой операции ([1]):")
        report.append("")

        report.append("С_Р = t_(g_i )/(F_g∙ K_V∙ K_P ),	(2)")
        report.append("где t_(g_i ) – трудоемкость i-той операций, ч.;")
        report.append("F_g – действительный фонд времени работы одного станка, ч;")
        report.append(f"F_g = {int(get_setting('fund_of_working'))} ч. − при двухсменном режиме работы;")
        report.append("K_V − коэффициент выполнения норм, принимается ориентировочно 1,1... 1,25; для станков с ЧПУ " "его следует принимать равным 1;")
        report.append(f"K_V = {get_setting('kv')}")
        report.append("K_P – коэффициент прогрессивности технологии проектируемого цеха;")
        report.append(f"K_P = {get_setting('kp')}")
        report.append("")

        report.append("Расчётное количество оборудования округляем до целого.")
        for operation in workshop.process.operations:
            operation_name = f"С_(Р {operation.number} {operation.name})"
            report_time = self.number_formatter.format(operation.time * Decimal(str(workshop.production_volume)))

            report.append(
                f"{operation_name} = {report_time} / ({get_setting('fund_of_working')} ∙ {get_setting('kv')} "
                f"∙ {get_setting('kp')}) = {self.number_formatter.format(operation.calculated_machines_count)}"
            )
            operation_name = f"С_(ПР {operation.number} {operation.name})"
            report.append(f"принимаем {operation_name} = {operation.accepted_machines_count}")

        report.append("")

        report.append("Коэффициент загрузки:")
        report.append("К_З = С_Р/С_ПРР")
        report.append("где С_Р − расчётное количество станков;")
        report.append("С_ПР − принятое количество станков.")
        for operation in workshop.process.operations:
            report.append(
                f"К_(З {operation.number} {operation.name}) = "
                f"{self.number_formatter.format(operation.calculated_machines_count)}/{operation.accepted_machines_count} = "
                f"{self.number_formatter.format(operation.calculated_machines_count / operation.accepted_machines_count)}"
            )
        report.append("")

        report.append("Средний коэффициент загрузки для всего станочного парка:")
        report.append("К_(З СР) = (∑С_Р)/(∑С_ПР )")
        report_list_load_factor = f"({self.number_formatter.format(workshop.process.operations[0].load_factor)}"
        for operation in workshop.process.operations[1:]:
            report_list_load_factor += f" + {self.number_formatter.format(operation.load_factor)}"
        report_list_load_factor += f")"
        report_list_count = f"({workshop.process.operations[0].accepted_machines_count}"
        for operation in workshop.process.operations[1:]:
            report_list_count += f" + {operation.accepted_machines_count}"
        report_list_count += f")"

        report.append(f"К_(З СР) = ({report_list_load_factor})/({report_list_count}) = " f"{self.number_formatter.format(workshop.process.average_load_factor)}")
        report.append("")
        report.append("Значения коэффициентов загрузки каждого станка, а также средний коэффициент загрузки заносим в" " таблицу 2.")

        report.append("")
        report.append("Таблица 2 - Необходимое количество станков и их загрузка")
        headers = ["№ и наименование операции", "Расчетное количество станков, ед", "Принятое количество станков, ед", "Коэффициент загрузки"]
        table_data = []
        for operation in workshop.process.operations:
            number = f"{operation.number} {operation.name}"
            calculated_machines_count = self.number_formatter.format(operation.calculated_machines_count)
            accepted_machines_count = operation.accepted_machines_count
            load_factor = self.number_formatter.format(operation.load_factor)
            table_data.append((number, calculated_machines_count, accepted_machines_count, load_factor))
        # Строка итога
        total_row = ('Итого', f'{workshop.process.total_machines_count}', f'{workshop.process.total_machines_count}', f'{self.number_formatter.format(workshop.process.average_load_factor)}')
        # Форматируем таблицу
        report.extend(self.table_formatter.format(headers, table_data, total_row))

        report.append("Для централизованной    переточки режущего инструмента в цехе организовывается заточное отделение. " "Основным оборудованием являются заточные станки:")
        rep_zone_percent = self.number_formatter.format(Decimal(get_setting('grinding_zone_percent')) * 100)
        rep_machines_count = workshop.process.total_machines_count
        rep_calc_count = workshop.zones["grinding_zone"].total_calculated_equipment_count
        rep_ac_count_1 = workshop.zones["grinding_zone"].total_equipment_count
        report.append(f"С_зат= {rep_zone_percent}% ∙ С_О	(5)")
        report.append("где С_О − число станков основного производства.")
        report.append(f"С_ЗАТ = {rep_zone_percent}% ∙ {rep_machines_count} = {self.number_formatter.format(rep_calc_count)}")
        report.append(f"принимаем С_(ПР ЗАТ) = {rep_ac_count_1}")
        report.append("")

        report.append("В состав цеха кроме заточного отделения может входить и ремонтное отделение. Количество станков " "ремонтного отделения можно принимать от числа обслуживаемых станков:")
        rep_repair_zone_percent = self.number_formatter.format(Decimal(get_setting('repair_zone_percent')) * 100)
        rep_calc_count = workshop.zones["repair_zone"].total_calculated_equipment_count
        rep_ac_count_2 = workshop.zones["repair_zone"].total_equipment_count
        report.append("где С_О − число станков основного производства.")
        report.append(f"С_рем = {rep_repair_zone_percent}% ∙ {rep_machines_count} = {self.number_formatter.format(rep_calc_count)}")
        report.append(f"принимаем С_(ПР РЕМ) = {rep_ac_count_2}")
        report.append("")

        report.append("Общее количество станков цеха:")
        report.append("С_ОБЩ = С_О+ С_(ПР ЗАТ)+ С_(ПР РЕМ)")
        report.append(f"С_ОБЩ = {rep_machines_count} + {rep_ac_count_1} + {rep_ac_count_2} = " f"{workshop.total_machines_count}")
        report.append("")

        report.append("Данные по принятому оборудованию производится в таблице 3.")
        report.append("Таблица 3 - Необходимое количество станков")
        headers = ["№ и наименование операции", "Наименование станков", "Количество, шт.", "Габаритные размеры, мм"]
        table_data = []
        for operation in workshop.process.operations:
            number = f"{operation.number} {operation.name}"
            length = self.number_formatter.format(operation.equipment.length * 1000)
            width = self.number_formatter.format(operation.equipment.width * 1000)
            height = self.number_formatter.format(operation.equipment.height * 1000)
            dimensions = f"{length} x {width} x {height}"
            table_data.append((number, operation.equipment.model, operation.accepted_machines_count, dimensions))
        # Строка итога
        total_row = ('', 'Итого', f'{workshop.total_machines_count}', '')
        # Форматируем таблицу
        report.extend(self.table_formatter.format(headers, table_data, total_row))
        report.append("")

        report.append("3. Расчёт площади участка")
        report.append("Определение размеров площади станочного отделения.")
        report.append("Площадь станочного отделения рассчитывается по формуле:")
        passage_area = get_setting('passage_area')
        report.append(f"S_СП = (a x b + {passage_area})∙C_ПР,")
        report.append("где a,b - габаритные размеры оборудования, м.;")
        report.append(f"{passage_area} – место на проходы;")
        report.append("С_ПР - принятое количество оборудования.")

        str_area_sum = ""
        for operation in workshop.process.operations:
            number = f"{operation.number} {operation.name}"
            length = self.number_formatter.format(operation.equipment.length)
            width = self.number_formatter.format(operation.equipment.width)
            area = self.number_formatter.format(operation.equipment.length * operation.equipment.width * operation.accepted_machines_count + passage_area)
            str_area_sum += f" + {area}"
            report.append(f"S_({number}) = ({length} ∙ {width} + {passage_area})∙ {operation.accepted_machines_count} " f"= {area}  м^2;")

        report.append("Суммарную площадь станочного отделения рассчитываем по формуле:")
        report.append("S_(СП) = ∑S_(СПi)")
        report.append(f"S_(СП) = {str_area_sum} = {self.number_formatter.format(workshop.zones['main_zone'].area)}  м^2;")

        report.append("")

        report.append("4. Корректировка компоновки технологического оборудования дополнительными площадями")
        report.append("Дополнительная площадь цеха складывается из:")
        report.append("")

        report.append("а) инструментально-раздаточной кладовой")
        report.append("Площадь склада инструмента:")
        report.append("S_(С.И.) = S_УД∙ C_ОБЩ,")
        report.append("где S_УД – удельная площадь склада инструмента на 1 станок, в зависимости от вида производства" " при работе в 2 смены, ;")
        rep_tool_storage = self.number_formatter.format(Decimal(get_setting('specific_areas.tool_storage')))
        report.append(f"S_УД = {rep_tool_storage} м^2;")
        report.append("C_ОБЩ – общее количество оборудования проектируемого участка.")
        report.append(f"S_(С.И.) = {rep_tool_storage} ∙ {workshop.total_machines_count} = " f"{self.number_formatter.format(workshop.zones['tool_storage_zone'].area)}  м^2")
        report.append("")

        report.append("б) склада приспособлений")
        report.append("Площадь склада приспособлений:")
        report.append("S_(С.П.) = S_УД∙ C_ОБЩ,")
        report.append("где S_УД – удельная площадь склада приспособлений на 1 станок;")
        rep_equipment_warehouse = self.number_formatter.format(Decimal(get_setting('specific_areas.equipment_warehouse')))
        report.append(f"S_УД = {rep_equipment_warehouse} м^2;")
        report.append(f"S_(С.П.) = {rep_equipment_warehouse} ∙ {workshop.total_machines_count} = " f"{self.number_formatter.format(workshop.zones['equipment_warehouse_zone'].area)}  м^2")
        report.append("")

        report.append("в) склада материалов и заготовок, межоперационных, готовых деталей")
        report.append("Площадь склада материалов и заготовок, межоперационных, готовых деталей:")
        work_piece_storage_percent = self.number_formatter.format(Decimal(get_setting('specific_areas.work_piece_storage')) * 100)
        report.append(f"Общая площадь промежуточных складов S_(С.К.П.) составляет {work_piece_storage_percent}% от " f"площади станочного отделения:")
        report.append(f"S_(С.К.П.) = {work_piece_storage_percent}% ∙ S_(УД СТ),")
        report.append(
            f"S_(С.К.П.) = {work_piece_storage_percent}% ∙ {self.number_formatter.format(workshop.zones['main_zone'].area)} "
            f"= {self.number_formatter.format(workshop.zones['work_piece_storage_zone'].area)}  м^2"
        )
        report.append("")

        report.append("г) контрольного отделения")
        report.append("Площадь контрольного отделения:")
        rep_control_department = self.number_formatter.format(Decimal(get_setting('specific_areas.control_department')))
        report.append(f"S_КОНТР = {rep_control_department} ∙ S_(УД СТ),")
        report.append(
            f"S_КОНТР = {rep_control_department} ∙ {self.number_formatter.format(workshop.zones['main_zone'].area)} "
            f"= {self.number_formatter.format(workshop.zones['control_department_zone'].area)}  м^2"
        )
        report.append("")

        report.append("д) санитарно-бытовых помещений")
        report.append("На проектируемом цехе предусматривается площадь, занимаемая двумя санитарными узлами по " "8 м^2 каждый.")
        rep_sanitary_zone = self.number_formatter.format(Decimal(get_setting('specific_areas.sanitary_zone')))
        report.append(f"S_САН = 2 ∙ {rep_sanitary_zone} = {self.number_formatter.format(workshop.zones['sanitary_zone'].area)} м^2")

        report.append("Размер дополнительной площади цеха составляет:")
        report.append("S_ДОП = S_(С.И.) + S_(С.П.) + S_(С.К.П.) + S_КОНТР + S_САН,")
        report.append(
            f"S_ДОП = {self.number_formatter.format(workshop.zones['tool_storage_zone'].area)} + "
            f"{self.number_formatter.format(workshop.zones['equipment_warehouse_zone'].area)} + "
            f"{self.number_formatter.format(workshop.zones['work_piece_storage_zone'].area)} + "
            f"{self.number_formatter.format(workshop.zones['control_department_zone'].area)} + "
            f"{self.number_formatter.format(workshop.zones['sanitary_zone'].area)} = "
            f"{self.number_formatter.format(workshop.required_area)} m^2"
        )

        report.append("")
        report.append("Общие размеры и площади цеха определяют на основе планирования оборудования и всех помещений " "участка.")
        report.append("Размеры пролета принимают в зависимости от рода машиностроения и характера выполняемых работ.")
        workshop_nam = get_setting('workshop_nam')
        workshop_span = get_setting('workshop_span')
        report.append(f"Принимаем ширину пролета цеха l = {workshop_span} м, число пролетов − {workshop_nam}.")
        report.append(
            "Длина пролета участка определяется суммой размеров производственных и вспомогательных "
            "отделений, последовательно расположенных вдоль пролета, проходов и других цехов участка. "
            "Основным размером, определяющим длину пролета, является длина технологической линии станков, "
            "расположенных вдоль пролета."
        )

        report.append("Длина пролёта:")
        report.append("L = S_Ц/l,")
        report.append("где L – длина пролета;")
        report.append("S_Ц – общая площадь участка;")
        report.append("l – суммарная ширина пролетов")
        report.append(f"L = {self.number_formatter.format(workshop.required_area)}/({workshop_span} ∙ {workshop_nam}) = " f"{self.number_formatter.format(workshop.length)} м,")
        report.append("")

        report.append("Таким образом, размеры цеха составляют:")
        report.append(f"ширина пролета l = {workshop_span} м,")
        report.append(f"число пролетов n = {workshop_nam},")
        report.append(f"длина пролета L = {self.number_formatter.format(workshop.length)} м.")
        report.append("Общая площадь цеха:")
        report.append(f"S_Ц = l ∙ n ∙ L,")
        report.append(f"S_Ц = {workshop_span} ∙ {workshop_nam} ∙ {self.number_formatter.format(workshop.length)} = " f"{self.number_formatter.format(workshop.total_area)} м^2")

        return "\n".join(report)

    def save_report(self, report: str, filepath: Path) -> bool:
        """
        Сохраняет отчет в текстовый файл.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(report)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении отчета: {str(e)}")
            return False
