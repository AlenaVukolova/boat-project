
class Oars:
    """Класс весла"""
    def __init__(self, first_oar_length: float, second_oar_length : float,\
                 first_oar_weight: float, second_oar_weight : float):
        """Инициализирует весел с указанными параметрами
        """
        self.oar1_length = first_oar_length     # длина первого весла 
        self.oar2_length = second_oar_length    # длина второго весла
        self.oar1_weight = first_oar_weight     # вес первого весла
        self.oar2_weight = second_oar_weight    # вес второго весла
        self.maximum_weight_of_one_oar = 3      # максимально допустимый вес одного весла в килограммах
        self.maximum_length = 2                 # максимально допустимая длина одного весла в метрах
        self.damages = {                        # словарь для учета повреждения для первого и второго весла
            'oar1': {},
            'oar2': {}
        }
        

    def velsa_are_the_same(self) -> bool:
        """Проверка, что весла одинаковые"""
        return self.oar1_length == self.oar2_length and self.oar1_weight == self.oar2_weight
    
    def permissible_weight(self) -> bool:
        """Проверка является ли вес весел в пределах допустимого"""      
        return self.oar1_weight + self.oar2_weight <= self.maximum_weight_of_one_oar * 2
    
    def oars_of_suitable_length(self) -> bool:
        """Проверка, что длина весел в пределах допустимого"""
        return self.oar1_length + self.oar2_length <= self.maximum_length * 2
    
    def add_damage(self, oar: str, location: str, severity: int) -> None:
        """
        Добавляет повреждение веслу.
        
        Args:
            oar: 'oar1' или 'oar2'
            location: 'blade' (лопасть), 'shaft' (древко), 'grip' (рукоять)
            severity: 1-3 (1 - царапина, 3 - поломка)
        """
        if oar not in ['oar1', 'oar2']:
            raise ValueError("Укажите 'oar1' или 'oar2'")
            
        if location not in ['blade', 'shaft', 'grip']:
            raise ValueError("Недопустимая локация повреждения")
            
        if not 1 <= severity <= 3:
            raise ValueError("Серьезность должна быть от 1 до 3")
            
        self.damages[oar][location] = self.damages[oar].get(location, 0) + severity

    def repair(self, oar: str, location: str, severity: int) -> None:
        """
        Ремонтирует повреждение весла.
        
        Args:
            oar: 'oar1' или 'oar2'
            location: Локация повреждения
            severity: Уровень ремонта (1-3)
        """
        if oar in self.damages and location in self.damages[oar]:
            self.damages[oar][location] = max(0, self.damages[oar][location] - severity)
            if self.damages[oar][location] == 0:
                del self.damages[oar][location]

    def has_critical_damages(self) -> bool:
        """Проверяет наличие критических повреждений (severity >= 2)."""
        for oar in ['oar1', 'oar2']:
            for severity in self.damages[oar].values():
                if severity >= 2:
                    return True
        return False

    def oars_are_suitable(self) -> bool:
        """
        Проверяет, пригодны ли весла для гребли.
        
        Returns:
            bool: True если весла одинаковые, без критических повреждений 
                  и параметры в допустимых пределах
        """
        
        return (self.velsa_are_the_same and self.permissible_weight()\
        and self.oars_of_suitable_length() and not self.has_critical_damages())

                    



a=Oars(2,2,1,1)
a.add_damage("oar1","blade",3)

            
    

    
    

        
    
    
    
        


