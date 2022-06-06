from dataclasses import dataclass
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Type

TrainingData = Tuple[str, Sequence[float]]
# Тип данных тренировки


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: ClassVar[str] = ('Тип тренировки: {}; '
                              'Длительность: {:.3f} ч.; '
                              'Дистанция: {:.3f} км; '
                              'Ср. скорость: {:.3f} км/ч; '
                              'Потрачено ккал: {:.3f}.')

    def get_message(self) -> str:
        format_message = self.message.format(self.training_type,
                                             self.duration,
                                             self.distance,
                                             self.speed,
                                             self.calories)
        return format_message


class Training:
    """Базовый класс тренировки.

    Порядок и назначение аргументов:
    action -- количество действий
    duration -- продолжительность
    weight -- вес спортсмена
    """

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self, data) -> None:
        self.action, self.duration, self.weight = data

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Определите ""get_spent_calories()"" в %s.'
            % (self.__class__.__name__))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_name = self.__class__.__name__
        distance = self.get_distance()
        mean_speed = self.get_mean_speed()
        spent_calories = self.get_spent_calories()
        info_message = InfoMessage(training_name,
                                   self.duration,
                                   distance,
                                   mean_speed,
                                   spent_calories)
        return info_message


class Running(Training):
    """Тренировка: бег."""

    COEFF_MEAN_SPEED_1: float = 18
    COEFF_MEAN_SPEED_2: float = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = self.duration * self.MIN_IN_HOUR
        coeff_mean_speed = (self.get_mean_speed()
                            * self.COEFF_MEAN_SPEED_1
                            - self.COEFF_MEAN_SPEED_2)
        spent_calories = (coeff_mean_speed
                          * self.weight
                          / self.M_IN_KM
                          * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.

    Порядок и назначение аргументов:
    ... -- аргументы базового класса
    height -- рост спортсмена
    """

    COEFF_CALORIE_1: float = 0.035
    COEFF_CALORIE_2: float = 0.029

    def __init__(self, data) -> None:
        super().__init__(data[:3])
        self.height = data[3]

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = (self.duration
                           * self.MIN_IN_HOUR)
        spent_calories = ((self.COEFF_CALORIE_1
                           * self.weight
                           + self.get_mean_speed()**2
                           // self.height
                           * self.COEFF_CALORIE_2
                           * self.weight)
                          * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание.

    Порядок и назначение аргументов:
    ... -- аргументы базового класса
    length_pool -- длина бассейна в метрах
    count_pool -- сколько раз пользователь переплыл бассейн
    """

    LEN_STEP: float = 1.38
    COEFF_MEAN_SPEED_1: float = 1.1
    COEFF_MEAN_SPEED_2: float = 2

    def __init__(self, data) -> None:
        super().__init__(data[:3])
        self.length_pool, self.count_pool = data[3:]

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        full_length_pool = self.length_pool * self.count_pool
        mean_speed = full_length_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + self.COEFF_MEAN_SPEED_1)
                          * self.COEFF_MEAN_SPEED_2
                          * self.weight)
        return spent_calories


def read_package(workout_type: str,
                 data: Sequence[float]) -> Optional[Training]:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    try:
        training = workout_types[workout_type](data)
        return training
    except KeyError:
        print(f'Несуществующий тип тренировки: ""{workout_type}""')
    except ValueError:
        print(f'Неверное количество данных: '
              f'Тренировка - "{workout_type}"; '
              f'Данные - {data}')
    return None


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages: List[TrainingData] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        if isinstance(training, Training):
            main(training)
