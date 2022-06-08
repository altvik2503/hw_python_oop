from dataclasses import (
    dataclass,
    asdict
)
from typing import (
    ClassVar,
    Dict,
    List,
    Sequence,
    Tuple,
    Type,
    Union
)

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
    message: ClassVar[str] = ('Тип тренировки: {training_type}; '
                              'Длительность: {duration:.3f} ч.; '
                              'Дистанция: {distance:.3f} км; '
                              'Ср. скорость: {speed:.3f} км/ч; '
                              'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        format_message = self.message.format(**asdict(self))
        return format_message


class Training:
    """Базовый класс тренировки.

    Порядок и назначение аргументов:
    action -- количество действий
    duration -- продолжительность
    weight -- вес спортсмена
    """

    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    MIN_IN_HOUR = 60.0

    def __init__(self, action, duration, weight) -> None:
        self.action, self.duration, self.weight = action, duration, weight

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
        classname = self.__class__.__name__
        error_message = f'Определите "get_spent_calories()" в {classname}'
        raise NotImplementedError(error_message)

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

    COEFF_MEAN_SPEED_1 = 18.0
    COEFF_MEAN_SPEED_2 = 20.0

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

    COEFF_CALORIE_1 = 0.035
    COEFF_CALORIE_2 = 0.029

    def __init__(self, action, duration, weight, height) -> None:
        super().__init__(action, duration, weight)
        self.height = height

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

    LEN_STEP = 1.38
    COEFF_MEAN_SPEED_1 = 1.1
    COEFF_MEAN_SPEED_2 = 2

    def __init__(self,
                 action,
                 duration,
                 weight,
                 length_pool,
                 count_pool
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
        spent_calories = ((mean_speed + self.COEFF_MEAN_SPEED_1)
                          * self.COEFF_MEAN_SPEED_2
                          * self.weight)
        return spent_calories


class TrainingNameErrorException(Exception):
    """Обработка ошибки типа тренировки"""

    pass


class TrainingDataErrorExcrption(Exception):
    """Обработка ошибки данных"""

    pass


def read_package(workout_type: str,
                 data: Sequence[Union[int, float]]
                 ) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking,
    }
    key_error_message = f'Несуществующий тип тренировки: "{workout_type}"'
    data_error_message = (f'Неверное количество данных: '
                          f'Тренировка - "{workout_type}"; '
                          f'Данные - {data}')
    try:
        training = workout_types[workout_type](*data)
        return training
    except KeyError:
        raise TrainingNameErrorException(key_error_message)
    except ValueError:
        raise TrainingDataErrorExcrption(data_error_message)


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
    error_message = 'Ошибка в данных тренировки: {}'
    for workout_type, data in packages:
        try:
            training = read_package(workout_type, data)
        except (TrainingDataErrorExcrption,
                TrainingNameErrorException) as ex:
            print(error_message.format(ex))
        else:
            main(training)
