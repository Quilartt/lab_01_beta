import sys

from toolkit.calculator import calculate
from toolkit.converter import convert
from toolkit.errors import ToolkitError

def main():
    if __name__ == '__main__':
        args = sys.argv[1:]
        if len(args) == 2:
            command = args[0]
            expression = args[1]
        elif len(args) == 6:
            command = args[0]
            value = args[1]
            from_unit = args[3]
            to_unit = args[5]
        elif len(args) == 1:
            command = args[0]
        else:
            raise ValueError("Ошибка ввода")
            
        if command == "calc":
            result = calculate(expression)
            print(result)

        elif command == "convert":
            result = convert(value, from_unit, to_unit)
            print(result)

        elif command == "--help":
            print("""
Использование:
python -m toolkit calc "EXPRESSION"
python -m toolkit convert VALUE --from UNIT --to UNIT
python -m toolkit --help

Единицы:
длина:          mm, cm, m, km
масса:          g, kg
температура:    c, f, k
""")

        else:
            raise ValueError("Ошибка ввода команды, доcступные: calc, convert, help")

        
if __name__ == "__main__":
    try: 
        main()
    except ToolkitError as e:
        print(e, file=sys.stderr)
        sys.exit(2)
