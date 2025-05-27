from frame import Frame

class AnchorSystem:
    """Класс якорной системы"""
    
    def __init__(self, depth_of_reservoir: float, length_of_rope: float, 
                 anchor_weight: float, frame: Frame):
        """
        Инициализирует якорную систему.
        
        Args:
            depth_of_reservoir: Глубина водоема в метрах
            length_of_rope: Длина веревки в метрах
            anchor_weight: Вес якоря в кг
            frame: Экземпляр класса Frame для доступа к параметрам лодки
        """
        self.frame = frame
        self.depth_of_reservoir = depth_of_reservoir
        self.length_of_rope = length_of_rope
        self.anchor_weight = anchor_weight
        self.rope_damage_level = 0  # 0-нет повреждений, 1-легкие, 2-критические
        self.anchor_damage_level = 0  # 0-нет повреждений, 1-легкие, 2-критические
        self.required_anchor_weight = frame.boat_length  # 1 кг на 1 метр длины лодки

    def check_rope_length(self) -> tuple[bool, str]:
        """
        Проверяет длину якорной веревки.
        
        Returns:
            tuple: (Статус проверки, Сообщение)
        """
        min_length = self.depth_of_reservoir * 3
        if self.length_of_rope >= min_length:
            return (True, "Якорная веревка достаточной длины")
        return (False, f"Веревка слишком короткая. Минимальная длина: {min_length} м")

    def check_anchor_weight(self) -> tuple[bool, str]:
        """
        Проверяет вес якоря.
        
        Returns:
            tuple: (Статус проверки, Сообщение)
        """
        if self.anchor_weight >= self.required_anchor_weight:
            return (True, "Якорь имеет достаточный вес")
        return (False, f"Вес якоря недостаточен. Требуется: {self.required_anchor_weight} кг")

    def add_rope_damage(self, severity: int) -> None:
        """
        Добавляет повреждение веревке.
        
        Args:
            severity: Уровень повреждения (1-легкое, 2-критическое)
        """
        if severity not in (1, 2):
            raise ValueError("Уровень повреждения должен быть 1 или 2")
        self.rope_damage_level = max(self.rope_damage_level, severity)

    def add_anchor_damage(self, severity: int) -> None:
        """
        Добавляет повреждение якорю.
        
        Args:
            severity: Уровень повреждения (1-легкое, 2-критическое)
        """
        if severity not in (1, 2):
            raise ValueError("Уровень повреждения должен быть 1 или 2")
        self.anchor_damage_level = max(self.anchor_damage_level, severity)

    def check_rope_condition(self) -> tuple[bool, str]:
        """
        Проверяет состояние якорной веревки.
        
        Returns:
            tuple: (Статус проверки, Сообщение)
        """
        if self.rope_damage_level == 0:
            return (True, "Веревка в хорошем состоянии")
        elif self.rope_damage_level == 1:
            return (True, "Веревка имеет незначительные повреждения")
        else:
            return (False, "Веревка имеет критические повреждения! Требуется замена")

    def check_anchor_condition(self) -> tuple[bool, str]:
        """
        Проверяет состояние якоря.
        
        Returns:
            tuple: (Статус проверки, Сообщение)
        """
        if self.anchor_damage_level == 0:
            return (True, "Якорь в хорошем состоянии")
        elif self.anchor_damage_level == 1:
            return (True, "Якорь имеет незначительные повреждения")
        else:
            return (False, "Якорь имеет критические повреждения! Требуется ремонт")

    def is_system_ok(self) -> tuple[bool, str]:
        """
        Комплексная проверка якорной системы.
        
        Returns:
            tuple: (Статус проверки, Сообщение)
        """
        checks = [
            self.check_rope_length(),
            self.check_anchor_weight(),
            self.check_rope_condition(),
            self.check_anchor_condition()
        ]
        
        for status, message in checks:
            if not status:
                return (False, message)
        return (True, "Якорная система в полном порядке")


        

                                                

       

