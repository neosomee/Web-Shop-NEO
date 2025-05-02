import pytest

from src.classes import Product, Category, Smartphone, LawnGrass
from unittest.mock import patch


def test_count_category():
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )
    assert category1.category_count == 1
    assert category1.product_count == 2
    product3 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product3],
    )
    assert category2.category_count == 2
    assert category2.product_count == 3
    product4 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category1.add_product(product4)
    assert category1.product_count == 4
    with pytest.raises(TypeError):
        category1.add_product({})


def test_init_product(product):
    assert product.name == "Iphone 16"
    assert product.description == "512GB, Gray space"
    assert product.price == 250000.0
    assert product.quantity == 7


def test_init_category(category):
    assert category.name == "Смартфоны"
    assert (
        category.description
        == "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни"
    )
    assert category.products == [
        "Samsung Galaxy S23 Ultra, 180000.0 руб. Остаток: 5 шт.\n",
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n",
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n",
    ]


def test_product_add_new():
    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    assert new_product.name == "Samsung Galaxy S23 Ultra"
    assert new_product.price == 180000.0


@patch("builtins.input", return_value="y")
def test_product_price_set(mock_input, capsys):
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    capsys.readouterr()
    product.price = -100
    captured = capsys.readouterr()
    assert "Цена не должна быть нулевая или отрицательная" in captured.out
    assert product.price == 210000.0  # Цена осталась прежней
    product.price = 1000
    assert product.price == 1000
    assert mock_input.call_count == 1
    mock_input.return_value = "n"
    product.price = 800
    assert product.price == 1000
    assert mock_input.call_count == 2

@patch("src.classes.Mixin.product_log", return_value = None)
def test_classes_methods(mock_product_log, capsys):
    product1 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product2 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)
    category = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2],
    )

    print(str(product1))
    captured = capsys.readouterr()
    assert captured.out == "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
    assert mock_product_log.call_count == 2  # Проверяем, что product_log вызван для product1 и product2

    print(str(product2))
    captured = capsys.readouterr()
    assert captured.out == "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"

    print(str(category))
    captured = capsys.readouterr()
    assert captured.out == "Смартфоны, количество продуктов: 22 шт.\n"

    assert product1 + product2 == 2114000.0


def test_smartphone_creation():
    phone = Smartphone(
        "Samsung Galaxy S23 Ultra",
        "256GB, Серый цвет",
        180000.0,
        5,
        95.5,
        "S23 Ultra",
        256,
        "Серый",
    )
    assert phone.name == "Samsung Galaxy S23 Ultra"
    assert phone.description == "256GB, Серый цвет"
    assert phone.price == 180000.0
    assert phone.quantity == 5
    assert phone.efficiency == 95.5
    assert phone.model == "S23 Ultra"
    assert phone.memory == 256
    assert phone.color == "Серый"


def test_lawngrass_creation():
    grass = LawnGrass(
        "Газонная трава",
        "Элитная трава для газона",
        500.0,
        20,
        "Россия",
        "7 дней",
        "Зеленый",
    )
    assert grass.name == "Газонная трава"
    assert grass.description == "Элитная трава для газона"
    assert grass.price == 500.0
    assert grass.quantity == 20
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


def test_product_addition():
    p1 = Product("Prod1", "Desc1", 1000.0, 2)  # 2000
    p2 = Product("Prod2", "Desc2", 2000.0, 3)  # 6000
    result = p1 + p2
    assert isinstance(result, (int, float))
    assert result == 8000.0


def test_smartphone_addition():
    phone1 = Smartphone("Phone1", "Desc1", 1000.0, 2, 90, "Model1", 64, "Black")
    phone2 = Smartphone("Phone2", "Desc2", 2000.0, 3, 85, "Model2", 128, "White")
    result = phone1 + phone2
    assert result == 8000.0


def test_lawngrass_addition():
    grass1 = LawnGrass("Grass1", "Desc1", 100.0, 10, "Country1", "5 дней", "Green")
    grass2 = LawnGrass("Grass2", "Desc2", 150.0, 15, "Country2", "7 дней", "Dark Green")
    result = grass1 + grass2
    assert result == 3250.0


