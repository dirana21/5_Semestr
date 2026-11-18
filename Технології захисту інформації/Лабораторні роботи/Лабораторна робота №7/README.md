# Лабораторна робота №7

Системи з відкритим ключем. Алгоритм RSA. Варіант 12.

- [Звіт](./Звіт.md)
- [Програма](./rsa.py)
- [Файли контрольного запуску](./example/)
- [Тести](./test_rsa.py)

Запуск із папки лабораторної. Для вихідних файлів потрібні нові імена.

```bash
python rsa.py encrypt example/Source.txt coded.txt
python rsa.py decrypt coded.txt restored.txt
python -m unittest -v
```
