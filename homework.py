"""Модуль фитнес-трекера."""
from dataclasses import dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        """Функция, возвращающая финальную строку с данными о тренировке."""
        return (f'Тип тренировки: {self.training_type};'
                f' Длительность: {self.duration:.3f} ч.;'
                f' Дистанция: {self.distance:.3f} км;'
                f' Ср. скорость: {self.speed:.3f} км/ч;'
                f' Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MINUTES_IN_HOUR: int = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        """Конструктор класса Training."""
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self):
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Возвращает потраченные ккал."""
        return (((self.CALORIES_MEAN_SPEED_MULTIPLIER
                  * super().get_mean_speed()
                  + self.CALORIES_MEAN_SPEED_SHIFT)
                 * self.weight / self.M_IN_KM * self.duration
                 * self.MINUTES_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_WEIGHT_MULTIPLIER: float = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: float = 0.029
    TRANSLATE_KM_HOUR_IN_METR_SEC: float = 0.278
    CENTIMETRE_IN_METR: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int):
        """Конструктор класса SportsWalking."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Функция по подсчету ккал."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((super().get_mean_speed()
                     * self.TRANSLATE_KM_HOUR_IN_METR_SEC) ** 2
                    / (self.height / self.CENTIMETRE_IN_METR))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MINUTES_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    ADDEND: float = 1.1
    MULTIPLIER: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        """Конструктор класса Swimming."""
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Длина_бассейна * count_pool / M_IN_KM / время_тренировки."""
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """(Средняя_скорость + 1.1) * 2 * вес * время_тренировки."""
        return ((self.get_mean_speed()
                 + self.ADDEND) * self.MULTIPLIER
                * self.weight * self.duration)


def read_package(work_type: str, dt: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_class: dict[str, type[Training]] = {
        'RUN': Running,
        'SWM': Swimming,
        'WLK': SportsWalking}
    return workout_type_class[work_type](*dt)


def main(tr: Training) -> None:
    """Главная функция."""
    info: InfoMessage = tr.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: list[tuple[str, list[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training: Training = read_package(workout_type, data)
        main(training)
