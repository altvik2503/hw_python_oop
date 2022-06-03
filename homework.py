class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,  # имя класса тренировки
                 duration: float,  # длительность тренировки в часах
                 distance: float,  # дистанция в километрах
                 speed: float,  # средняя скорость
                 calories: float  # количество килокалорий
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        message = (f'Тип тренировки: {self.training_type}; '
                   f'Длительность: {self.duration:0.3f} ч.; '
                   f'Дистанция: {self.distance:.3f} км;')
        return message


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_HOUR = 60

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
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
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info_message = InfoMessage(self.__class__.__name__,
                                   self.duration,
                                   self.get_distance(),
                                   self.get_mean_speed(),
                                   self.get_spent_calories())
        return info_message


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        duration_in_min = self.duration * self.MIN_IN_HOUR
        spent_calories = ((coeff_calorie_1
                           * self.get_mean_speed()
                           - coeff_calorie_2)
                          * self.weight
                          / self.M_IN_KM
                          * duration_in_min)
        return spent_calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 height: float  # рост спортсмена
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 0.035  # коэффициент 1
        coeff_calorie_2 = 0.029  # коэффициент 2
        duration_in_min = (self.duration
                           * self.MIN_IN_HOUR)  # длительность в минутах
        spent_calories = ((coeff_calorie_1
                           * self.weight
                           + self.get_mean_speed()**2
                           // self.height
                           * coeff_calorie_2
                           * self.weight)
                          * duration_in_min)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,  # количество совершённых действий
                 duration: float,  # длительность тренировки
                 weight: float,  # вес спортсмена
                 length_pool: float,  # длина бассейна
                 count_pool: float  # количество проплытых бассейнов
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
        coeff_calorie_1 = 1.1
        coeff_calorie_2 = 2
        spent_calories = ((self.get_mean_speed()
                           + coeff_calorie_1)
                          * coeff_calorie_2
                          * self.weight)
        return spent_calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_types = {'SWM': Swimming,  # плаванье
                     'RUN': Running,  # бег
                     'WLK': SportsWalking  # спортивная ходьба
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
