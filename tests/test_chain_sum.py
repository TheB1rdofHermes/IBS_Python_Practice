from Practice_4.chain_sum import chain_sum


def test_chain_sum():
    assert chain_sum(5)() == 5                         # Проверка chain_sum(5)()
    assert chain_sum(5)(2)() == 7                      # Проверка chain_sum(5)(2)()
    assert chain_sum(5)(100)(-10)() == 95             # Проверка chain_sum(5)(100)(-10)()
