from dataclasses import dataclass, asdict
from typing import List, ClassVar, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    MESSAGE: ClassVar[str] = ("Тип тренировки: {training_type}; "
                              "Длительность: {duration:.3f} ч.; "
                              "Дистанция: {distance:.3f} км; "
                              "Ср. скорость: {speed:.3f} км/ч; "
                              "Потрачено ккал: {calories:.3f}.")

    def get_message(self):
        return self.MESSAGE.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки."""

    action: int
    duration: float
    weight: float

    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[int] = 1000
    MIN_IN_HOUR: ClassVar[int] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


@dataclass
class Running(Training):
    """Тренировка: бег."""

    RATIO_RUN_1: ClassVar[int] = 18
    RATIO_RUN_2: ClassVar[int] = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для RUN."""
        return((self.RATIO_RUN_1 * self.get_mean_speed() - self.RATIO_RUN_2)
               * self.weight / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    height: float

    RATIO_WLK_1: ClassVar[int] = 0.035
    RATIO_WLK_2: ClassVar[int] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для WLK."""
        return((self.RATIO_WLK_1 * self.weight
               + (self.get_mean_speed()**2 // self.height) * self.RATIO_WLK_2
               * self.weight) * self.duration * self.MIN_IN_HOUR)


@dataclass
class Swimming(Training):
    """Тренировка: плавание."""

    length_pool: float
    count_pool: float

    LEN_STEP: ClassVar[float] = 1.38
    RATIO_SWM_1: ClassVar[float] = 1.1
    RATIO_SWM_2: ClassVar[int] = 2

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения для SWM."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий для SWM"""
        return(self.get_mean_speed()
               + self.RATIO_SWM_1) * self.RATIO_SWM_2 * self.weight


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    type_train = {"RUN": Running,
                  "SWM": Swimming,
                  "WLK": SportsWalking}
    try:
        return type_train[workout_type](*data)
    except KeyError:
        raise ValueError('Такой тренировки не существует')


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Dict[str, type[Training]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
