# SOLID Showcase

[![Відкрити інтерактивну демонстрацію](https://img.shields.io/badge/Відкрити_в_браузері-SOLID_Showcase-E8734A?style=for-the-badge)](https://dirana21.github.io/5_Semestr/)

Лабораторна робота №1 демонструє п'ять принципів SOLID на трьох незалежних предметних областях. Основна програма створена на WPF, а браузерна версія на Blazor WebAssembly використовує те саме C# ядро.

## Реалізовані завдання

1. **Data Import Pipeline** — імпорт CSV та JSON, валідація транзакцій, репозиторій, прогрес і підсумковий звіт.
2. **Каталог бібліотеки** — книги, газети, альманахи, тестова ініціалізація, додавання, видалення та пошук.
3. **Автобаза** — заявки на перевезення, підбір водія й автомобіля, рейси, поломки, ремонт і виплати.

Після кожної дії права панель показує:

- послідовність викликів класів і методів;
- фрагмент C# коду з активним рядком;
- використаний принцип `S`, `O`, `L`, `I` або `D`;
- пояснення архітектурного рішення.

## Ручний режим

Окрім готових демонстраційних сценаріїв, у кожному модулі можна працювати зі своїми даними:

- вставити власний CSV або JSON із транзакціями;
- створити книгу, газету чи альманах, відредагувати або видалити видання та виконати пошук;
- додати водіїв і автомобілі, сформувати власну заявку на перевезення та простежити призначення рейсу.

Кожна ручна операція також формує покрокову трасу SOLID.

## Структура рішення

```text
SolidShowcase.sln
├── src/SolidShowcase.Core
│   ├── DataImport
│   │   ├── Contracts, Models, Parsers, Readers
│   │   └── Repositories, Reporting, Services, Validation
│   ├── Library
│   │   ├── Contracts, Models, Factories, Repositories
│   │   └── Search, Services
│   ├── MotorPool
│   │   ├── Contracts, Models, Repositories
│   │   └── Strategies, Services
│   ├── Demo
│   └── Shared
├── src/SolidShowcase.Wpf     основний Windows інтерфейс
├── src/SolidShowcase.Web     браузерна демонстрація
└── tests/SolidShowcase.Tests модульні тести
```

У ядрі діє правило **один тип — один файл**: кожний інтерфейс, клас,
запис і перелік зберігається окремо. Назва файла збігається з назвою типу.

Докладне зіставлення принципів із класами наведено у [документі про архітектуру](docs/SOLID.md).

## Запуск WPF

Потрібні Windows та .NET 9 SDK.

```powershell
dotnet run --project "src/SolidShowcase.Wpf/SolidShowcase.Wpf.csproj"
```

## Локальний запуск браузерної версії

```powershell
dotnet run --project "src/SolidShowcase.Web/SolidShowcase.Web.csproj"
```

## Перевірка

```powershell
dotnet test SolidShowcase.sln
```

Публікація GitHub Pages виконується автоматично workflow `solid-showcase-pages.yml` після зміни лабораторної роботи в гілці `main`.
