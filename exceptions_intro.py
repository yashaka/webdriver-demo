from typing import Optional, Tuple, Generic, TypeVar

MAX = 100


class Error(Exception):
    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return self.message


# TypeOfResult = TypeVar('TypeOfResult')
# TypeOfError = TypeVar('TypeOfError')
#
#
# class Either(Generic[TypeOfResult, TypeOfError]):
#     def __init__(self, result: TypeOfResult=None, error: TypeOfError=None):
#         self.maybe_result = result
#         self.maybe_error = error
#
# def fraction(x: int, y: int) -> Either[str, Error]:
#     if y == 0:
#         return Either(error=Error('cannot devide by zero'))
#     elif y > 100:
#         return Either(error=Error(f'cannot have so big number: {y}'))
#     else:
#         return Either(result=f'{x}/{y}')


def fraction(x: int, y: int) -> str:
    if y == 0:
        raise ArithmeticError('cannot devide by zero')
    elif y > 100:
        raise ArithmeticError(f'cannot have so big number: {y}')
    else:
        return f'{x}/{y}'

# def count(number: int, parts: int, whole: int) -> Either[str, Error]:
#     fractionOrError = fraction(whole, parts)
#     if fractionOrError.maybe_error:
#         return Either(error=fractionOrError.maybe_error)
#     elif number == 0:
#         return Either(error=Error('number cannot be zero'))
#     else:
#         return Either(result=f'{number}x({fractionOrError.maybe_result})')


def count(number: int, parts: int, whole: int) -> str:
    try:
        fract = fraction(whole, parts)
    except Error as error:
        raise Error(f'failed build fraction: reason: {error}')
    if number == 0:
        raise Error('number of count cannot be zero')
    else:
        return f'{number}x({fract})'


# countOrError = count(0, 0, 1)
#
# if countOrError.maybe_error:
#     print(f'ERROR: {countOrError.maybe_error}!!!')
# else:
#     print(repr(countOrError.maybe_result))

try:
    print(repr(count(0, 2, 1)))
except Error as error:
    # print(f'ERROR: {error}!!!')
    print(error)
