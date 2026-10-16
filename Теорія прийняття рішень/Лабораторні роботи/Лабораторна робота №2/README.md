# Лабораторна робота № 2

**Дисципліна:** Теорія прийняття рішень<br>
**Тема:** Обчислення середньої та медіанної оцінок на шкалі рангів<br>
**Варіант:** 12<br>
**Мова програмування:** C#<br>
**Виконав:** Левченко Д. В., КН-24-1<br>
**Перевірила:** доцент кафедри Рилова Н. В.

## Результат

За середніми та медіанними ранговими оцінками отримано однаковий порядок альтернатив: **4 → 3 → 2 → 1**. Коефіцієнт конкордації `W = 0,7`, тому думки експертів достатньо узгоджені.

- [Звіт для перегляду на GitHub](./Звіт.md)
- [Звіт Word](./Звіт_ЛР2_Левченко.docx)
- [Вихідний код](./DecisionTheoryLab2/)
- [Автоматичні перевірки](./DecisionTheoryLab2.Tests/)
- [Таблиця результатів CSV](./results/lab2-results.csv)

## Запуск

```powershell
dotnet build .\DecisionTheoryLab2.sln -c Release
dotnet run --project .\DecisionTheoryLab2\DecisionTheoryLab2.csproj -c Release
dotnet run --project .\DecisionTheoryLab2.Tests\DecisionTheoryLab2.Tests.csproj -c Release
```

## Структура

```text
Лабораторна робота №2/
├── DecisionTheoryLab2/          # консольна програма C#
├── DecisionTheoryLab2.Tests/    # автоматичні перевірки
├── results/                     # підсумкова таблиця CSV
├── screenshots/                 # скриншоти виконання
├── Звіт.md                      # версія звіту для GitHub
└── Звіт_ЛР2_Левченко.docx       # звіт у форматі Word
```
