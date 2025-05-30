#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------------------------------------------------
import textwrap
from decimal import Decimal
from pathlib import Path

from design_of_mechanical_production.core.entities.workshop import Workshop
from design_of_mechanical_production.core.interfaces import INumberFormatter, IReportGenerator, ITableFormatter
from design_of_mechanical_production.data.output.formatters import NumberFormatter, TableFormatter
from design_of_mechanical_production.settings import get_setting


class TextReportGenerator(IReportGenerator):
    """
    Класс для генерации текстовых отчетов.
    """

    def __init__(self, number_formatter: INumberFormatter = None, table_formatter: ITableFormatter = None):
        self.number_formatter = number_formatter or NumberFormatter()
        self.fn = self.number_formatter.format
        self.table_formatter = table_formatter or TableFormatter()
        self.ft = self.table_formatter.format

    def generate_report(self, workshop: Workshop) -> str:
        """
        Генерирует текстовый отчет о цехе.
        """
        report = list()
        report.append(f"Отчет по цеху: {workshop.name}")

        report.append(f"1. Исходные данные:")
        report.append("")
        report_total_time = self.fn(workshop.process.total_time)
        report.append(f"Трудоемкость изготовления 1го изделия − {report_total_time} нормо-часа.")
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
            number = str(operation.number)
            percentage = f"{self.fn(operation.percentage)}%"
            time = str(self.fn(operation.time))
            table_data.append((number, operation.name, percentage, time))
        # Строка итога
        workshop_total_time = self.fn(workshop.process.total_time)
        total_row = ('-', '-', 'Итого', workshop_total_time)
        # Форматируем таблицу
        report.extend(self.ft(headers, table_data, total_row))

        report.append("")

        report.append("2. Расчётное количество станков на каждой операции ([1]):")
        report.append("")

        report.append("С_Р = t_(g_i )/(F_g∙ K_V∙ K_P ),	(2)")
        report.append("где t_(g_i ) – трудоемкость i-той операций, ч.;")
        report.append("F_g – действительный фонд времени работы одного станка, ч;")
        report.append(f"F_g = {int(get_setting('fund_of_working'))} ч. − при двухсменном режиме работы;")
        report.append(
            "K_V − коэффициент выполнения норм, принимается ориентировочно 1,1... 1,25; для станков с ЧПУ "
            "его следует принимать равным 1;"
        )
        report.append("K_P – коэффициент прогрессивности технологии проектируемого цеха;")
        report.append(f"K_P = {get_setting('kp')}")
        report.append("")

        report.append("Расчётное количество оборудования округляем до целого.")
        for operation in workshop.process.operations:
            operation_name = f"С_(Р {operation.number} {operation.name})"
            report_time = self.fn(operation.time)
            report.append(
                f"{operation_name} = {report_time} / ({get_setting('fund_of_working')} ∙ {get_setting('kv')} "
                f"∙ {get_setting('kp')}) = {self.fn(operation.calculated_equipment_count)}"
            )
            operation_name = f"С_(ПР {operation.number} {operation.name})"
            report.append(f"принимаем {operation_name} = {operation.accepted_equipment_count}")

        report.append("")

        report.append("Коэффициент загрузки:")
        report.append("К_З = С_Р/С_ПРР")
        report.append("где С_Р − расчётное количество станков;")
        report.append("С_ПР − принятое количество станков.")
        for operation in workshop.process.operations:
            report.append(
                f"К_(З {operation.number} {operation.name}) = "
                f"{self.fn(operation.calculated_equipment_count)}/{operation.accepted_equipment_count} = "
                f"{self.fn(operation.load_factor)}"
            )
        report.append("")

        report.append("Средний коэффициент загрузки для всего станочного парка:")
        report.append("К_(З СР) = (∑С_Р)/(∑С_ПР )")
        report_list_load_factor = f"({self.fn(workshop.process.operations[0].load_factor)}"
        report_list_count = f"({workshop.process.operations[0].accepted_equipment_count}"
        for operation in workshop.process.operations[1:]:
            report_list_load_factor += f" + {self.fn(operation.load_factor)}"
            report_list_count += f" + {operation.accepted_equipment_count}"
        report_list_load_factor += f")"
        report_list_count += f")"

        average_load_factor = self.fn(workshop.process.average_load_factor)
        report.append(
            f"К_(З СР) = ({report_list_load_factor})/({report_list_count}) = {average_load_factor}"
        )
        report.append("")
        report.append("Значения коэффициентов загрузки каждого станка, а также средний коэффициент загрузки заносим в "
                      "таблицу 2.")

        report.append("")
        report.append("Таблица 2 - Необходимое количество станков и их загрузка")
        headers = [
            "№ и наименование операции",
            "Расчетное количество станков, ед",
            "Принятое количество станков, ед",
            "Коэффициент загрузки",
        ]
        table_data = []
        for operation in workshop.process.operations:
            number = f"{operation.number} {operation.name}"
            calculated_machines_count = self.fn(operation.calculated_equipment_count)
            accepted_machines_count = operation.accepted_equipment_count
            load_factor = self.fn(operation.load_factor)
            table_data.append((number, calculated_machines_count, accepted_machines_count, load_factor))
        calculated_machines_count = self.fn(workshop.process.calculated_machines_count)
        average_load_factor = self.fn(workshop.process.average_load_factor)
        total_row = (
            'Итого',
            f'{calculated_machines_count}',
            f'{workshop.process.accepted_machines_count}',
            f'{average_load_factor}',
        )
        # Форматируем таблицу
        report.extend(self.table_formatter.format(headers, table_data, total_row))

        report.append("")
        report.append("Данные по принятому оборудованию производится в таблице 3.")
        report.append("")

        report.append("Таблица 3 - Необходимое количество станков")
        headers = ["№ и наименование операции", "Наименование станков", "Количество, шт.", "Габаритные размеры, мм"]
        table_data = []
        for operation in workshop.process.operations:
            number = f"{operation.number} {operation.name}"
            length = self.fn(operation.equipment.length * 1000)
            width = self.fn(operation.equipment.width * 1000)
            height = self.fn(operation.equipment.height * 1000)
            dimensions = f"{length} x {width} x {height}"
            table_data.append((number, operation.equipment.model, operation.accepted_equipment_count, dimensions))
        # Строка итога
        total_row = ('-', 'Итого', f'{workshop.zones["main_zone"].accepted_machines_count}', '-')
        # Форматируем таблицу
        report.extend(self.table_formatter.format(headers, table_data, total_row))
        report.append("")

        report.append("Для централизованной переточки режущего инструмента в цехе организовывается заточное отделение. "
                      "Основным оборудованием являются заточные станки:")
        rep_zone_percent = self.fn(Decimal(get_setting('grinding_zone_percent')) * 100)
        rep_machines_count = workshop.process.accepted_machines_count
        rep_calc_count = workshop.zones["grinding_zone"].calculated_machines_count
        rep_ac_count_1 = workshop.zones["grinding_zone"].accepted_machines_count
        report.append(f"С_зат= {rep_zone_percent}% ∙ С_О	(5)")
        report.append("где С_О − число станков основного производства.")
        report.append(
            f"С_ЗАТ = {rep_zone_percent}% ∙ {rep_machines_count} = {self.fn(rep_calc_count)}"
        )
        report.append(f"принимаем С_(ПР ЗАТ) = {rep_ac_count_1}")
        report.append("")

        report.append(
            "В состав цеха кроме заточного отделения может входить и ремонтное отделение. Количество станков "
            "ремонтного отделения можно принимать от числа обслуживаемых станков:"
        )
        rep_repair_zone_percent = self.fn(Decimal(get_setting('repair_zone_percent')) * 100)
        rep_calc_count = workshop.zones["repair_zone"].calculated_machines_count
        rep_ac_count_2 = workshop.zones["repair_zone"].accepted_machines_count
        report.append("где С_О − число станков основного производства.")
        report.append(
            f"С_рем = {rep_repair_zone_percent}% ∙ {rep_machines_count} = "
            f"{self.fn(rep_calc_count)}"
        )
        report.append(f"принимаем С_(ПР РЕМ) = {rep_ac_count_2}")
        report.append("")

        report.append("Общее количество станков цеха:")
        report.append("С_ОБЩ = С_О + С_(ПР ЗАТ) + С_(ПР РЕМ)")
        report.append(
            f"С_ОБЩ = {rep_machines_count} + {rep_ac_count_1} + {rep_ac_count_2} = " f"{workshop.total_machines_count}"
        )
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
            length = self.fn(operation.equipment.length)
            width = self.fn(operation.equipment.width)
            area = self.fn(
                operation.equipment.length * operation.equipment.width * operation.accepted_equipment_count
                + passage_area
            )
            str_area_sum += f"{area} + "
            report.append(
                f"S_({number}) = ({length} ∙ {width} + {passage_area}) ∙ {operation.accepted_equipment_count} "
                f"= {area} м²;"
            )

        report.append("Суммарную площадь станочного отделения рассчитываем по формуле:")
        report.append("S_СП = ∑S_СПi + S_ЗАТ + S_РЕМ")
        str_area_sum += f"{self.fn(workshop.zones['grinding_zone'].area)} + "
        str_area_sum += f"{self.fn(workshop.zones['repair_zone'].area)}"
        report.append(
            f"S_СП = {str_area_sum} = {self.fn(workshop.zones['main_zone'].area)} м²;"
        )

        report.append("")

        report.append("4. Корректировка компоновки технологического оборудования дополнительными площадями")
        report.append("Дополнительная площадь цеха складывается из:")
        report.append("")

        report.append("а) инструментально-раздаточной кладовой")
        report.append("Площадь склада инструмента:")
        report.append("S_(С.И.) = S_УД∙ C_ОБЩ,")
        report.append(
            "где S_УД – удельная площадь склада инструмента на 1 станок, в зависимости от вида производства"
            " при работе в 2 смены;"
        )
        rep_tool_storage = self.fn(Decimal(get_setting('specific_areas.tool_storage')))
        report.append(f"S_УД = {rep_tool_storage} м²;")
        report.append("C_ОБЩ – общее количество оборудования проектируемого участка.")
        report.append(
            f"S_(С.И.) = {rep_tool_storage} ∙ {workshop.total_machines_count} = "
            f"{self.fn(workshop.zones['tool_storage_zone'].area)} м²"
        )
        report.append("")

        report.append("б) склада приспособлений")
        report.append("Площадь склада приспособлений:")
        report.append("S_(С.П.) = S_УД∙ C_ОБЩ,")
        report.append("где S_УД – удельная площадь склада приспособлений на 1 станок;")
        rep_equipment_warehouse = self.fn(
            Decimal(get_setting('specific_areas.equipment_warehouse'))
        )
        report.append(f"S_УД = {rep_equipment_warehouse} м²;")
        report.append(
            f"S_(С.П.) = {rep_equipment_warehouse} ∙ {workshop.total_machines_count} = "
            f"{self.fn(workshop.zones['equipment_warehouse_zone'].area)} м²"
        )
        report.append("")

        report.append("в) склада материалов и заготовок, межоперационных, готовых деталей")
        report.append("Площадь склада материалов и заготовок, межоперационных, готовых деталей:")
        work_piece_storage_percent = self.fn(
            Decimal(get_setting('specific_areas.work_piece_storage')) * 100
        )
        report.append(
            f"Общая площадь промежуточных складов S_(С.К.П.) составляет {work_piece_storage_percent}% от "
            f"площади станочного отделения:"
        )
        report.append(f"S_(С.К.П.) = {work_piece_storage_percent}% ∙ S_(УД СТ),")
        report.append(
            f"S_(С.К.П.) = {work_piece_storage_percent}% ∙ "
            f"{self.fn(workshop.zones['main_zone'].area)} "
            f"= {self.fn(workshop.zones['work_piece_storage_zone'].area)} м²"
        )
        report.append("")

        report.append("г) контрольного отделения")
        report.append("Площадь контрольного отделения:")
        rep_control_department = self.fn(Decimal(get_setting('specific_areas.control_department')))
        report.append(f"S_КОНТР = {rep_control_department} ∙ S_(УД СТ),")
        report.append(
            f"S_КОНТР = {rep_control_department} ∙ {self.fn(workshop.zones['main_zone'].area)} "
            f"= {self.fn(workshop.zones['control_department_zone'].area)} м²"
        )
        report.append("")

        report.append("д) санитарно-бытовых помещений")
        report.append(
            "На проектируемом цехе предусматривается площадь, занимаемая двумя санитарными узлами по 8 м² каждый."
        )
        rep_sanitary_zone = self.fn(Decimal(get_setting('specific_areas.sanitary_zone')))
        report.append(
            f"S_САН = 2 ∙ {rep_sanitary_zone} = {self.fn(workshop.zones['sanitary_zone'].area)} м²"
        )
        report.append("")

        report.append("Размер дополнительной площади цеха составляет:")
        report.append("S_ДОП = S_(С.И.) + S_(С.П.) + S_(С.К.П.) + S_КОНТР + S_САН,")
        report.append(
            f"S_ДОП = {self.fn(workshop.zones['tool_storage_zone'].area)} + "
            f"{self.fn(workshop.zones['equipment_warehouse_zone'].area)} + "
            f"{self.fn(workshop.zones['work_piece_storage_zone'].area)} + "
            f"{self.fn(workshop.zones['control_department_zone'].area)} + "
            f"{self.fn(workshop.zones['sanitary_zone'].area)} = "
            f"{self.fn(workshop.required_area_additional_zones)} м²"
        )
        report.append("")

        report.append("Общий размер площади цеха составляет:")
        report.append("S = S_СП + S_ДОП,")
        report.append(
            f"S = {self.fn(workshop.required_area_main_zone)} + "
            f"{self.fn(workshop.required_area_additional_zones)} = "
            f"{self.fn(workshop.required_area)} м²"
        )
        report.append("")

        report.append("5. Окончательная компоновка цеха. ")
        report.append("Общие размеры и площади цеха определяют на основе планирования оборудования и всех помещений.")
        report.append("Размеры пролета принимают в зависимости от рода машиностроения и характера выполняемых работ.")
        workshop_nam = get_setting('workshop_nam')
        workshop_span = get_setting('workshop_span')
        report.append(f"Принимаем ширину пролета цеха l = {workshop_span} м, число пролетов = {workshop_nam}.")
        report.append(
            "Длина пролета участка определяется суммой размеров производственных и вспомогательных "
            "отделений, последовательно расположенных вдоль пролета, проходов и других цехов участка. "
            "Основным размером, определяющим длину пролета, является длина технологической линии станков, "
            "расположенных вдоль пролета."
        )

        report.append("Длина пролёта:")
        report.append("L_(РАСЧ) = S_Ц/l,")
        report.append("где S_Ц – общая площадь участка;")
        report.append("l – суммарная ширина пролетов, которая определяется по формуле:")
        report.append("l = l_1 ∙ n,")
        report.append(f"где l_1 = {workshop_span} – ширина одного пролета;")
        report.append(f"где n = {workshop_nam} – количество пролетов.")
        report.append("Таким образом, длина пролёта определяется по формуле:")
        report.append("L_(РАСЧ) = S_Ц/(l_1 ∙ n),")
        report.append(
            f"L_(РАСЧ) = {self.fn(workshop.required_area)}/({workshop_span} ∙ {workshop_nam}) = "
            f"{self.fn(workshop.calculated_length)} м,"
        )
        report.append("Расчетную длину пролетов округляем до большего целого числа, кратного 6.")
        report.append(f"Принимаем: L = {self.fn(workshop.length)}")
        report.append("")

        report.append("Таким образом, размеры цеха составляют:")
        report.append(f"    - ширина одного пролета l_1 = {workshop_span} м,")
        report.append(f"    - число пролетов n = {workshop_nam},")
        report.append(f"    - принятая длина пролета L = {self.fn(workshop.length)} м.")
        report.append("Общая площадь цеха:")
        report.append(f"S_Ц = l ∙ n ∙ L,")
        report.append(
            f"S_Ц = {workshop_span} ∙ {workshop_nam} ∙ {self.fn(workshop.length)} = "
            f"{self.fn(workshop.total_area)} м²"
        )

        return "\n".join(report)

    def save_report(self, report: str, filepath: Path) -> bool:
        """
        Сохраняет отчет в текстовый файл.
        """
        try:
            # Разбиваем текст на строки и обрабатываем каждую отдельно
            wrapped_lines = []
            for line in report.splitlines():
                if line.strip() == "":  # Если строка пустая
                    wrapped_lines.append("")  # Добавляем пустую строку как есть
                else:
                    # Оборачиваем непустую строку с максимальной шириной 120 символов
                    wrapped_lines.extend(textwrap.wrap(line, width=120))
            
            # Собираем обратно в текст, сохраняя переносы строк
            wrapped_report = '\n'.join(wrapped_lines)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(wrapped_report)
            return True
        except Exception as e:
            print(f"Ошибка при сохранении отчета: {str(e)}")
            return False
