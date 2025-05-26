from ..boat.oars import Oars
import pytest

@pytest.fixture
def sample_oars():
    """Фикстура для создания экземпляра Oars"""
    return Oars(
        first_oar_length=1.8,
        second_oar_length=1.8,
        first_oar_weight=1.5,
        second_oar_weight=1.5
    )

class TestOars:
    def test_initialization(self, sample_oars):
        """Тест корректности инициализации"""
        assert sample_oars.oar1_length == 1.8
        assert sample_oars.oar2_length == 1.8
        assert sample_oars.oar1_weight == 1.5
        assert sample_oars.oar2_weight == 1.5
        assert sample_oars.damages == {'oar1': {}, 'oar2': {}}

    def test_velsa_are_the_same(self, sample_oars):
        """Тест проверки идентичности весел"""
        assert sample_oars.velsa_are_the_same() is True
        
        # Проверка на неидентичных веслах
        diff_oars = Oars(1.8, 2.0, 1.5, 1.5)
        assert diff_oars.velsa_are_the_same() is False

    def test_permissible_weight(self):
        """Тест проверки допустимого веса"""
        # Нормальный вес
        oars = Oars(1.8, 1.8, 1.5, 1.5)
        assert oars.permissible_weight() is True
        
        # Превышение веса
        heavy_oars = Oars(1.8, 1.8, 3.0, 3.0)
        assert heavy_oars.permissible_weight() is False

    def test_oars_of_suitable_length(self):
        """Тест проверки допустимой длины"""
        # Нормальная длина
        oars = Oars(1.8, 1.8, 1.5, 1.5)
        assert oars.oars_of_suitable_length() is True
        
        # Слишком длинные весла
        long_oars = Oars(2.5, 2.5, 1.5, 1.5)
        assert long_oars.oars_of_suitable_length() is False

    def test_add_damage(self, sample_oars):
        """Тест добавления повреждений"""
        sample_oars.add_damage('oar1', 'blade', 1)
        assert sample_oars.damages['oar1']['blade'] == 1
        
        sample_oars.add_damage('oar1', 'blade', 2)
        assert sample_oars.damages['oar1']['blade'] == 3  # 1 + 2

    def test_repair(self, sample_oars):
        """Тест ремонта повреждений"""
        sample_oars.add_damage('oar1', 'shaft', 2)
        sample_oars.repair('oar1', 'shaft', 1)
        assert sample_oars.damages['oar1']['shaft'] == 1
        
        sample_oars.repair('oar1', 'shaft', 1)
        assert 'shaft' not in sample_oars.damages['oar1']

    def test_has_critical_damages(self, sample_oars):
        """Тест проверки критических повреждений"""
        assert sample_oars.has_critical_damages() is False
        
        sample_oars.add_damage('oar2', 'grip', 2)
        assert sample_oars.has_critical_damages() is True

    def test_oars_are_suitable(self, sample_oars):
        """Тест общей пригодности весел"""
        assert sample_oars.oars_are_suitable() is True
        
        # Добавляем критическое повреждение
        sample_oars.add_damage('oar1', 'blade', 3)
        assert sample_oars.oars_are_suitable() is False

    @pytest.mark.parametrize("oar,location,severity", [
        ('oar3', 'blade', 1),  # Неправильное весло
        ('oar1', 'handle', 1),  # Неправильная локация
        ('oar1', 'blade', 0),   # Слишком низкая серьезность
        ('oar1', 'blade', 4)    # Слишком высокая серьезность
    ])
    def test_invalid_damage(self, sample_oars, oar, location, severity):
        """Тест на недопустимые параметры повреждений"""
        with pytest.raises(ValueError):
            sample_oars.add_damage(oar, location, severity)