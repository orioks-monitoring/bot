from abc import ABCMeta


class CheckBaseException(Exception, metaclass=ABCMeta):
    """Абстрактное исключение, наследники которого возникают при ошибках во время проверки."""
