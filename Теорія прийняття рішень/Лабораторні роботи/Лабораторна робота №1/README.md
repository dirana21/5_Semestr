# Лабораторна робота № 1

**Дисципліна:** Теорія прийняття рішень  
**Тема:** Багатокритеріальні задачі прийняття рішень. Формування множини Парето  
**Варіант:** 12  
**Мова програмування:** C#  
**Виконав:** Левченко Д. В., КН-24-1  
**Перевірила:** доцент кафедри Рилова Н. В.

## Результат

Програма сформувала 15 альтернатив, визначила множину Парето `{1, 4, 8, 9, 13, 15}`, виконала зважування й нормування критеріїв та обрала **об'єкт № 4** з максимальним значенням функції корисності `F = 1,4174`.

- [Звіт, що відображається на GitHub](./Звіт.md)
- [Звіт Word](./Звіт_ЛР1_Левченко.docx)
- [Вихідний код](./DecisionTheoryLab1/)
- [Автоматичні перевірки](./DecisionTheoryLab1.Tests/)
- [Таблиця результатів CSV](./results/pareto-results.csv)

## Запуск

Потрібен .NET SDK 8 або новіший.

```powershell
dotnet build .\DecisionTheoryLab1.sln -c Release
dotnet run --project .\DecisionTheoryLab1\DecisionTheoryLab1.csproj -c Release
dotnet run --project .\DecisionTheoryLab1.Tests\DecisionTheoryLab1.Tests.csproj -c Release
```

## Структура

```text
Лабораторна робота №1/
├── DecisionTheoryLab1/          # консольна програма C#
├── DecisionTheoryLab1.Tests/    # автономні автоматичні перевірки
├── results/                     # CSV та протоколи запуску
├── screenshots/                 # скриншоти виконання
├── Звіт.md                      # версія звіту для GitHub
└── Звіт_ЛР1_Левченко.docx       # звіт у форматі Word
```
