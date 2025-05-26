import pytest
from ..boat.frame import Frame
from ..boat.anchor import AnchorSystem

# Фикстуры для тестов
@pytest.fixture
def sample_frame():
    """Фикстура для создания экземпляра Frame."""
    return Frame(boat_length=5.0, max_load=200)

@pytest.fixture
def sample_anchor(sample_frame):
    """Фикстура для создания экземпляра AnchorSystem."""
    return AnchorSystem(
        depth_of_reservoir=10,
        length_of_rope=35,
        anchor_weight=5.0,
        frame=sample_frame
    )

# Тесты для AnchorSystem
class TestAnchorSystem:
    def test_initialization(self, sample_anchor, sample_frame):
        """Тест корректности инициализации."""
        assert sample_anchor.depth_of_reservoir == 10
        assert sample_anchor.length_of_rope == 35
        assert sample_anchor.anchor_weight == 5.0
        assert sample_anchor.frame == sample_frame
        assert sample_anchor.rope_damage_level == 0
        assert sample_anchor.anchor_damage_level == 0

    @pytest.mark.parametrize("depth,rope_len,expected", [
        (10, 30, (True, "Якорная веревка достаточной длины")),
        (10, 20, (False, "Веревка слишком короткая. Минимальная длина: 30 м")),
        (5, 10, (False, "Веревка слишком короткая. Минимальная длина: 15 м")),
    ])
    def test_check_rope_length(self, sample_frame, depth, rope_len, expected):
        """Параметризованный тест проверки длины веревки."""
        anchor = AnchorSystem(depth, rope_len, 5.0, sample_frame)
        assert anchor.check_rope_length() == expected

    @pytest.mark.parametrize("weight,expected", [
        (5.0, (True, "Якорь имеет достаточный вес")),
        (3.0, (False, "Вес якоря недостаточен. Требуется: 5.0 кг")),
        (10.0, (True, "Якорь имеет достаточный вес")),
    ])
    def test_check_anchor_weight(self, sample_frame, weight, expected):
        """Параметризованный тест проверки веса якоря."""
        anchor = AnchorSystem(10, 35, weight, sample_frame)
        assert anchor.check_anchor_weight() == expected

    @pytest.mark.parametrize("severity,expected", [
        (1, (True, "Веревка имеет незначительные повреждения")),
        (2, (False, "Веревка имеет критические повреждения! Требуется замена")),
    ])
    def test_rope_damage(self, sample_anchor, severity, expected):
        """Тест добавления повреждений веревки."""
        sample_anchor.add_rope_damage(severity)
        assert sample_anchor.check_rope_condition() == expected

    @pytest.mark.parametrize("severity,expected", [
        (1, (True, "Якорь имеет незначительные повреждения")),
        (2, (False, "Якорь имеет критические повреждения! Требуется ремонт")),
    ])
    def test_anchor_damage(self, sample_anchor, severity, expected):
        """Тест добавления повреждений якоря."""
        sample_anchor.add_anchor_damage(severity)
        assert sample_anchor.check_anchor_condition() == expected

    def test_invalid_damage_level(self, sample_anchor):
        """Тест на недопустимый уровень повреждений."""
        with pytest.raises(ValueError, match="Уровень повреждения должен быть 1 или 2"):
            sample_anchor.add_rope_damage(3)
        with pytest.raises(ValueError, match="Уровень повреждения должен быть 1 или 2"):
            sample_anchor.add_anchor_damage(0)

    @pytest.mark.parametrize("rope_dmg,anchor_dmg,expected", [
        (0, 0, (True, "Якорная система в полном порядке")),
        (1, 0, (True, "Якорная система в полном порядке")),
        (0, 1, (True, "Якорная система в полном порядке")),
        (2, 0, (False, "Веревка имеет критические повреждения! Требуется замена")),
        (0, 2, (False, "Якорь имеет критические повреждения! Требуется ремонт")),
    ])
    def test_is_system_ok(self, sample_anchor, rope_dmg, anchor_dmg, expected):
        """Комплексная проверка системы с разными повреждениями."""
        if rope_dmg > 0:
            sample_anchor.add_rope_damage(rope_dmg)
        if anchor_dmg > 0:
            sample_anchor.add_anchor_damage(anchor_dmg)
        assert sample_anchor.is_system_ok() == expected