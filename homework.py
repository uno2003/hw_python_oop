from dataclasses import dataclass, asdict
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Возвращает сообщение о тренировке."""
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Базовый класс тренировки.
    Константы:
    M_IN_KM метров в километре
    LEN_STEP длинна шага
    MIN_IN_HOUR минут в часе
    """

    M_IN_KM: ClassVar[int] = 1000
    LEN_STEP: ClassVar[float] = 0.65
    MIN_IN_HOUR: ClassVar[float] = 60.0

    action: int
    duration: float
    weight: float

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError('Определите get_spent_calories в %s.'
                                  % (type(self).__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           duration=self.duration,
                           distance=self.get_distance(),
                           speed=self.get_mean_speed(),
                           calories=self.get_spent_calories()
                           )


@dataclass
class Running(Training):
    """Тренировка: бег.
    Константы:
    CALORIES_MEAN_SPEED_MULTIPLIER коэффициент для множителя средней скорости
    CALORIES_MEAN_SPEED_SHIFT коэффициент для сдвига средней скорости
    """

    CALORIES_MEAN_SPEED_MULTIPLIER: float = 18.0
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий (бег)."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                 * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * self.duration * self.MIN_IN_HOUR
                )


@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
    Константы:
    CALORIES_WEIGHT_MULTIPLIER коэффициент для множителя веса спортсмена
    CALORIES_SPEED_HEIGHT_MULTIPLIER коэффициент для множителя частного
                                     квадрата средней скорости
                                     и роста спортсмена
    KMH_IN_MSEC коэффициент для перевода значений из км/ч в м/с
    CM_IN_M сантиметров в метрах
    POWER возведение в степень
    """

    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER: ClassVar[float] = 0.029
    KMH_IN_MSEC: ClassVar[float] = 0.278
    CM_IN_M: ClassVar[float] = 100.0
    POWER: ClassVar[float] = 2.0

    action: int
    duration: float
    weight: float
    height: float

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий (спортивная ходьба)."""
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.KMH_IN_MSEC * self.get_mean_speed()) ** self.POWER
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight)
                * (self.MIN_IN_HOUR * self.duration))


@dataclass
class Swimming(Training):
    """Тренировка: плавание.
    Константы:
    LEN_STEP вместо шага - гребок
    CALORIES_MEAN_SPEED_SHIFT коэффициент для смещения
                              значения средней скорости
    CALORIES_WEIGHT_MULTIPLIER коэффициент для множителя скорости
    """

    LEN_STEP: ClassVar[float] = 1.38
    CALORIES_MEAN_SPEED_SHIFT: ClassVar[float] = 1.1
    CALORIES_WEIGHT_MULTIPLIER: ClassVar[float] = 2.0

    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: float

    def get_mean_speed(self) -> float:
        """Возвращает среднюю скорость плавания."""
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        """Возвращает количество затраченных калорий (плавание)."""
        return ((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.CALORIES_WEIGHT_MULTIPLIER
                * self.weight * self.duration
                )


def read_package(workout_type: str, data: list[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        return training[workout_type](*data)
    except KeyError as error_message:
        print(f'Тип тренеровки, {error_message} не найден')


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
