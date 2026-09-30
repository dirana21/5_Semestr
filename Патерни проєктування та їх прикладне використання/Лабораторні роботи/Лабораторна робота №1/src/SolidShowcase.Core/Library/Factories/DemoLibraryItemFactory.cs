namespace SolidShowcase.Core;

public sealed class DemoLibraryItemFactory(SolidTracer tracer) : ILibraryItemFactory
{
    private int _index;

    public LibraryItem CreateRandom()
    {
        tracer.Add(
            "Каталог бібліотеки",
            "Створення випадкового видання",
            "DemoLibraryItemFactory.CreateRandom()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "Фабрика повертає базовий LibraryItem. Новий тип видання додається окремим класом без зміни CatalogService.",
            "public LibraryItem CreateRandom()\n{\n    return variants[_index++ % variants.Length]();\n}",
            3);

        Func<LibraryItem>[] variants =
        [
            () => new Book(Guid.NewGuid(), "Чистий код", 2008, "Prentice Hall", "Роберт Мартін", "Програмування", 464),
            () => new Newspaper(Guid.NewGuid(), "Tech Weekly", 2026, "Campus Press", 42, new DateOnly(2026, 9, 30), "Наука — Олена; ІТ — Андрій"),
            () => new Almanac(Guid.NewGuid(), "Українська фантастика", 2024, "Навчальна книга", "Фантастика", ["Місто", "Острів", "Сигнал"])
        ];

        return variants[_index++ % variants.Length]();
    }
}
