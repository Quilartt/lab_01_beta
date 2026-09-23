class ToolkitError(Exception):
    pass


class EmptyExpression(ToolkitError):
    pass


class UnknownSymbol(ToolkitError):
    pass


class MissingOperand(ToolkitError):
    pass


class TwoOperators(ToolkitError):
    pass


class DivisionByZero(ToolkitError):
    pass


class UnknownUnit(ToolkitError):
    pass


class IncompatibleUnits(ToolkitError):
    pass


class InvalidValue(ToolkitError):
    pass


class AbsoluteZeroException(ToolkitError):
    pass


class InvalidNumber(ToolkitError):
    pass