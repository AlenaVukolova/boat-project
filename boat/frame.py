class Frame:
    """Класс корпуса лодки"""   
    def __init__(self, boat_length: float, max_load: float):
        """Инициализирует корпус с указанными параметрами"""
        self.waterproof = True                   # водонепроницаемость лодки
        self.boat_length = boat_length           # длина корпуса лодки в метрах
        self.max_load = max_load                 # максимальная нагрузка в килограммах 
        self.damages = {}                        # словарь повреждений в формате {'location': severity}
        self.total_weight = 0                    # общий вес груза в лодки в килограммах
                  
      
    def add_damage(self, location: str, severity: int) -> None:
        """
        Добавляет повреждение с указанием локации и серьёзности.
        
        :param location: 'bottom' (дно), 'side' (борт), 'bow' (нос), 'stern' (корма)
        :param severity: 1-3 (1 - царапина, 2 - трещина, 3 - пробоина)
        """
        if location not in self.damages:
            self.damages[location] = 0
        self.damages[location] += severity
        self._update_waterproof_status()
    
    def repair(self, location: str, severity: int) -> None:
        """Ремонтирует лодку"""
        if location in self.damages:
            self.damages[location] = max(0, self.damages[location] - severity)
            if self.damages[location] == 0:
                del self.damages[location]
            self._update_waterproof_status()
    
    def _update_waterproof_status(self) -> None:
        """Обновляет статус герметичности на основе повреждений."""
        self.waterproof = True  # Сначала предполагаем, что лодка герметична
        
        for location, severity in self.damages.items():
            if location == 'bottom' and severity >= 2:
                self.waterproof = False
                break
            elif location in ('side', 'bow', 'stern') and severity >= 3:
                self.waterproof = False
                break    

    def is_waterproof(self) -> bool:
        """Проверяет текущий статус герметичности."""
        return self.waterproof

    def add_cargo(self, cargo : int) -> None:
        """Добавление груза"""
        if cargo < 0:
            raise ValueError("Вес не может быть отрицательным")
        self.total_weight += cargo
    
    def removal_of_cargo(self, cargo : int) -> None:
        """Удаление груза"""
        if cargo < 0:
            raise ValueError("Вес не может быть отрицательным")
        self.total_weight -= cargo

    def buoyancy_check(self) -> tuple[bool, str] :
        """Проверка плавучести"""
        if self.total_weight <= self.max_load:
            return (True, "Груз в допустимых пределах, лодка не тонет")
        return (False, "Перегруз. Лодка скоро затонет" )

        


    




 