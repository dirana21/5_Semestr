# Лабораторна робота №11. Перевірка цілісності через SHA-256

[Звіт із покроковим прикладом, результатами та скриншотами](./Звіт.md)

Потрібен Python 3.10 або новіший. Модуль `hashlib` входить до стандартної бібліотеки.

## Запуск

У PowerShell із папки лабораторної:

```powershell
$expected = python sha256_check.py ./samples/before.txt
python sha256_check.py ./samples/before.txt --expected $expected
python sha256_check.py ./samples/after.txt --expected $expected
```

Перша команда обчислює еталон. Наступні дві перевіряють початковий та змінений вміст. Код завершення `0` означає успішне обчислення або збіг, `1` — розбіжність, `2` — помилку введення або читання.

| Файл | Призначення |
|---|---|
| [sha256_check.py](./sha256_check.py) | Обчислення й порівняння SHA-256 |
| [before.txt](./samples/before.txt) | Початковий зразок `Items: 10` |
| [after.txt](./samples/after.txt) | Зразок після зміни `Items: 11` |
