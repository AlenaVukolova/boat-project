from ..boat.frame import Frame
import pytest

def test_frame_initialization():
    """Тест корректности создания объекта Frame и начальных значений"""
    frame = Frame(boat_length=5.0, max_load=200)
    
    # Проверка начальных значений
    assert frame.boat_length == 5.0
    assert frame.max_load == 200
    assert frame.waterproof is True  # Лодка должна быть герметична при создании
    assert frame.total_weight == 0   # Начальный вес груза должен быть 0
    assert frame.damages == {}       # Словарь повреждений должен быть пустым



def test_damage_system():
    """Тест добавления повреждений и их влияния на герметичность"""
    frame = Frame(boat_length=3.0, max_load=150)
    
    # Добавляем легкое повреждение дна (severity=1)
    frame.add_damage("bottom", 1)
    assert frame.is_waterproof() is True  # Лодка должна остаться герметичной
    
    # Добавляем критическое повреждение борта (severity=3)
    frame.add_damage("side", 3)
    assert frame.is_waterproof() is False  # Теперь лодка течет
    
    # Ремонтируем повреждение
    frame.repair("side", 2)  # Уменьшаем severity с 3 до 1
    assert frame.is_waterproof() is True  # После ремонта снова герметична

def test_cargo_system():
    """Тест добавления/удаления груза и проверки плавучести"""
    frame = Frame(boat_length=4.0, max_load=300)
    
    # Добавляем груз
    frame.add_cargo(150)
    assert frame.total_weight == 150
    status, msg = frame.buoyancy_check()
    assert status is True  # Груз в пределах нормы
    
    # Добавляем еще груз (превышаем лимит)
    frame.add_cargo(160)
    assert frame.total_weight == 310
    status, msg = frame.buoyancy_check()
    assert status is False  # Перегруз!
    assert "затонет" in msg  # Проверяем текст предупреждения
    
    # Пробуем добавить отрицательный вес
    with pytest.raises(ValueError):
        frame.add_cargo(-50)  # Должно вызвать ошибку    