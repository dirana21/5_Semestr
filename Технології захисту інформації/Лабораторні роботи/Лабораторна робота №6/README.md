# Лабораторна робота №6

DES у режимі CBC. Варіант 4 (номер за списком 12).

- [Звіт](./Звіт.md)
- [Алгоритм DES](./des.py) і [стандартні таблиці](./des_tables.py)
- [Файлова програма DES-CBC](./des_cbc.py)
- [Файли контрольного запуску](./example/)
- [Тести](./test_des.py)

Запуск із папки лабораторної. Вихідні файли створюються за новими іменами.

```bash
python des_cbc.py encrypt example/Source.txt coded.bin --key 0123456789ABCDEF --iv 1234567890ABCDEF
python des_cbc.py decrypt coded.bin restored.txt --key 0123456789ABCDEF --iv 1234567890ABCDEF
python -m unittest -v
```
