

def check_fields_in_dict(field_1, field_2, dct):
    """
    Проверяет наличие ключей в словаре
    и значения этих ключей на тип str
    :param field_1: искомый ключ
    :param field_2: искомый ключ
    :param dct: словарь
    :return: список значений этих ключей
    """
    if field_1 in dct and field_2 in dct:
        if isinstance(field_1, str) and isinstance(field_2, str):
            result = [dct[field_1], dct[field_2]]
            return result



