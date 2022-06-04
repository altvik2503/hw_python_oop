from dataclasses import dataclass
from typing import ClassVar


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float
    message: ClassVar[str] = ('Тип тренировки: {:.3f}; '
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
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000
    MIN_IN_HOUR: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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
            'Определите ""get_spent_calories()"" в %s.' % (self.__class__.__name__))

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
    """Тренировка: спортивная ходьба."""

    coeff_calorie_1: float = 0.035
    coeff_calorie_2: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_in_min = (self.duration
                           * self.MIN_IN_HOUR)
        spent_calories = ((self.coeff_calorie_1
                           * self.weight
                           + self.get_mean_speed()**2
                           // self.height
                           * self.coeff_calorie_2
                           * self.weight)
                          * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    coeff_mean_speed_1: float = 1.1
    coeff_mean_speed_2: float = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        full_length_pool = self.length_pool * self.count_pool
        mean_speed = full_length_pool / self.M_IN_KM / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        mean_speed = self.get_mean_speed()
        spent_calories = ((mean_speed + self.coeff_mean_speed_1)
                          * self.coeff_mean_speed_2
                          * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming,
                     'RUN': Running,
                     'WLK': SportsWalking
                     }
    if workout_type == 'SWM':
        training = workout_types[workout_type](data[0],
                                               data[1],
                                               data[2],
                                               data[3],
                                               data[4])
    elif workout_type == 'RUN':
        training = workout_types[workout_type](data[0],
                                               data[1],
                                               data[2])
    elif workout_type == 'WLK':
        training = workout_types[workout_type](data[0],
                                               data[1],
                                               data[2],
                                               data[3])
    else:
        training = Training(data[0],
                            data[1],
                            data[2])
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    message = info.get_message()
    print(message)


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
