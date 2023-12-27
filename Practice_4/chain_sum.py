# Определение класса chain_sum, который создает цепную функцию суммирования
class chain_sum:
    def __init__(self, num):
        self.num = num

    def __call__(self, value=None):
        if value is None:
            return self.num
        else:
            return chain_sum(self.num + value)



