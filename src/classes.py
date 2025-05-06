from abc import ABC, abstractmethod

class BaseProduct(ABC):
    @abstractmethod
    def __init__(self, name, description, price, quantity):
        self.name = name
        self.description = description
        self._price = price
        self.quantity = quantity

    @abstractmethod
    def new_product(self):
        pass

    @abstractmethod
    def __str__(self):
        pass

    def __add__(self, other):
        pass

class Mixin:
    def __init__(self):
        super().__init__()
        self.product_log()

    def product_log(self):
        print(f'{self.__class__.__name__}({self.name}, {self.description}, {self.price}, {self.quantity})')

class Product(Mixin, BaseProduct):
    name: str
    description: str
    price: float
    quantity: int

    def __init__(self, name, description, price, quantity):
        BaseProduct.__init__(self, name, description, price, quantity)
        Mixin.product_log(self)
        if quantity <= 0:
            raise ValueError("Товар с нулевым количеством не может быть добавлен")
        else:
            self.quantity = quantity

    def __str__(self):
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other):
        if type(self) != type(other):
            raise TypeError
        sum1 = self.price * self.quantity
        sum2 = other.price * other.quantity
        return sum1 + sum2

    @classmethod
    def new_product(cls, params: dict):
        return cls(**params)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, new_price):
        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            if new_price < self._price:
                ans = input("Вы ввели цену ниже прошлой, подтвердите изменение цены (y/n,да/нет)")
                if ans.lower() == "y":
                    self._price = new_price
            else:
                self._price = new_price


class Smartphone(Product):
    def __init__(
        self, name, description, price, quantity, efficiency, model, memory, color
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    def __init__(
        self, name, description, price, quantity, country, germination_period, color
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    name: str
    description: str
    products: list
    product_count = 0
    category_count = 0

    def __init__(self, name, description, products=None):
        self.name = name
        self.description = description
        self.__products = []
        if products:
            for i in products:
                self.add_product(i)
        Category.category_count += 1

    def __str__(self):
        total_quantity = 0
        for i in self.__products:
            total_quantity += i.quantity
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def add_product(self, product):
        if not isinstance(product, Product):
            raise TypeError("Нельзя добавлять объекты не типа Класс")
        else:
            self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self):
        my_list = []
        for i in self.__products:
            my_list.append(f"{i.name}, {i.price} руб. Остаток: {i.quantity} шт.\n")
        return my_list

    def middle_price(self):
        try:
            product_count = len(self.__products)
            sum = 0
            for i in self.__products:
                sum += i.price

            return sum / product_count
        except ZeroDivisionError:
            return 0
