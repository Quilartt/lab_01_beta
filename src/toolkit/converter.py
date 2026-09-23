from .errors import IncompatibleUnits,AbsoluteZeroException, InvalidValue, UnknownUnit

dict_length = {"km": 1000, "m": 1, "cm": 0.01, "mm": 0.001}

dict_mass = {"g": 1, "kg": 1000}

dict_temp = {"c", "f", "k"}


def convert_from_c(value: float, to_unit: str) -> float:
    if value + 273.15 < 0:
        raise AbsoluteZeroException("Температура меньше абсолютного 0")
    elif to_unit == "k":
        result = value + 273.15
    elif to_unit == "f":
        result = value*9/5+32
    else:
        result = value
    return result


def convert(value: str, from_unit: str, to_unit: str) -> float:
    from_unit = from_unit.lower()
    to_unit = to_unit.lower()
    try:
        value = float(value)
    except (TypeError, ValueError) as exc:
        raise InvalidValue(f"Недопустимое значение: {value}") from exc

    known = set(dict_length) | set(dict_mass) | dict_temp
    if from_unit not in known:
        raise UnknownUnit("Недопустимая единица измерения", from_unit)
    if to_unit not in known:
        raise UnknownUnit("Недопустимая единица измерения", to_unit)
    
    if from_unit in dict_length:
        if to_unit in dict_length:
            result = dict_length[from_unit]/dict_length[to_unit]*value
        else: 
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")

    if from_unit in dict_mass:
        if to_unit in dict_mass:
            result = dict_mass[from_unit]/dict_mass[to_unit]*value
        else: 
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")

    if from_unit in dict_temp:
        if to_unit not in dict_temp:
            raise IncompatibleUnits(f"Невозможен перевод из {from_unit} в {to_unit}")
        else:
            if from_unit == "c":
                result = convert_from_c(value, to_unit)
            elif from_unit == "k":
                temp_c = value - 273.15
                result = convert_from_c(temp_c, to_unit)
            elif from_unit == "f":
                temp_c = (value - 32) * 5 / 9
                result = convert_from_c(temp_c, to_unit)
    return result








