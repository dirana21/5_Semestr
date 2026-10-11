# Лабораторна робота № 1 з NoSQL баз даних

**Варіант:** 5  
**Виконав:** студент групи КН-24-1 Левченко Д. В.  
**Перевірив:** Андреєв П. І.

## Результат

Створено документну базу даних `nosql_lab1_variant5` для навчального портфоліо. База містить 7 колекцій по 10 документів. Дані про дисципліни та лабораторні роботи сформовано на основі матеріалів інших предметів у репозиторії.

| Колекція | Кількість документів | Призначення |
|---|---:|---|
| `disciplines` | 10 | дисципліни та технології |
| `students` | 10 | студенти й портфоліо |
| `teachers` | 10 | викладачі та дисципліни |
| `laboratory_works` | 10 | лабораторні роботи з різних предметів |
| `assignments` | 10 | вимоги до робіт |
| `submissions` | 10 | подання робіт у репозиторії |
| `grades` | 10 | стани перевірки та структура оцінювання |

## Структура каталогу

```text
Лабораторна робота №1/
├── data/
│   └── disciplines.json
├── scripts/
│   ├── init_portfolio.js
│   └── verify_portfolio.js
├── screenshots/
│   ├── 01-collections-overview.png
│   ├── 02-imported-discipline.png
│   ├── 03-students-insert-methods.png
│   └── 04-laboratory-works.png
├── Звіт.md
└── Звіт_ЛР1_Левченко.docx
```

## Відтворення бази

1. Запустити локальний MongoDB Server.
2. Імпортувати колекцію `disciplines` за допомогою `mongoimport`:

```powershell
mongoimport --uri "mongodb://127.0.0.1:27017" --db "nosql_lab1_variant5" --collection "disciplines" --file ".\data\disciplines.json" --jsonArray
```

3. Створити решту колекцій і індексів. У сценарії використано `insertOne()` та `insertMany()`:

```powershell
mongosh "mongodb://127.0.0.1:27017" --file ".\scripts\init_portfolio.js"
```

4. Перевірити кількість колекцій і документів:

```powershell
mongosh "mongodb://127.0.0.1:27017" --file ".\scripts\verify_portfolio.js"
```

## Звіт

- [Звіт у форматі Markdown](./Звіт.md)
- [Звіт у форматі Word](./Звіт_ЛР1_Левченко.docx)

