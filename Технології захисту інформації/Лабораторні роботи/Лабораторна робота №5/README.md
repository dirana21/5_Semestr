# Лабораторна робота №5

Шифрування методом гамування. Варіант 12.

- [Звіт](./Звіт.md)
- [Датчики гами](./generators.py)
- [Шифратор і дешифратор](./gamma_cipher.py)
- [Файли контрольного запуску](./example/)
- [Тести](./test_gamma_cipher.py)

Запуск із папки лабораторної.

```bash
python generators.py
python gamma_cipher.py encrypt example
python gamma_cipher.py decrypt example
python -m unittest -v
```

Команди шифрування і дешифрування перезаписують відповідно `Coded.txt` і `DeCoded.txt` у вказаній папці. Шифротекст має двійковий формат. Його шістнадцяткове подання наведено у звіті.
