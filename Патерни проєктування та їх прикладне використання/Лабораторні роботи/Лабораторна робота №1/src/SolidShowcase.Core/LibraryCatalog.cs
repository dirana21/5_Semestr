namespace SolidShowcase.Core;

public abstract record LibraryItem(Guid Id, string Title, int Year, string Publisher)
{
    public abstract string Kind { get; }
    public abstract string Details { get; }
}

public sealed record Book(Guid Id, string Title, int Year, string Publisher, string Author, string Genre, int Pages)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Книга";
    public override string Details => $"{Author}, {Genre}, {Pages} стор.";
}

public sealed record Newspaper(Guid Id, string Title, int Year, string Publisher, int IssueNumber, DateOnly ReleaseDate, string Columns)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Газета";
    public override string Details => $"№{IssueNumber}, {ReleaseDate:dd.MM.yyyy}; {Columns}";
}

public sealed record Almanac(Guid Id, string Title, int Year, string Publisher, string Genre, IReadOnlyList<string> Works)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Альманах";
    public override string Details => $"{Genre}; твори: {string.Join(", ", Works)}";
}

public interface ICatalogRepository
{
    IReadOnlyList<LibraryItem> GetAll();
    void Add(LibraryItem item);
    bool Update(LibraryItem item);
    bool Remove(Guid id);
}

public interface ILibrarySearchStrategy
{
    string Name { get; }
    bool Matches(LibraryItem item, string query);
}

public interface ILibraryItemFactory
{
    LibraryItem CreateRandom();
}

public sealed class InMemoryCatalogRepository : ICatalogRepository
{
    private readonly List<LibraryItem> _items = [];

    public IReadOnlyList<LibraryItem> GetAll() => _items;
    public void Add(LibraryItem item) => _items.Add(item);
    public bool Update(LibraryItem item)
    {
        var index = _items.FindIndex(existing => existing.Id == item.Id);
        if (index < 0) return false;
        _items[index] = item;
        return true;
    }
    public bool Remove(Guid id) => _items.RemoveAll(item => item.Id == id) > 0;
}

public sealed class TitleSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за назвою";
    public bool Matches(LibraryItem item, string query) => item.Title.Contains(query, StringComparison.OrdinalIgnoreCase);
}

public sealed class PublisherSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за видавництвом";
    public bool Matches(LibraryItem item, string query) => item.Publisher.Contains(query, StringComparison.OrdinalIgnoreCase);
}

public sealed class AuthorSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за автором";
    public bool Matches(LibraryItem item, string query) => item is Book book && book.Author.Contains(query, StringComparison.OrdinalIgnoreCase);
}

public sealed class YearSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за роком";
    public bool Matches(LibraryItem item, string query) => item.Year.ToString() == query.Trim();
}

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

public sealed class CatalogService(
    ICatalogRepository repository,
    ILibraryItemFactory factory,
    SolidTracer tracer)
{
    public IReadOnlyList<LibraryItem> Items => repository.GetAll();

    public void Add(LibraryItem item)
    {
        tracer.Add(
            "Каталог бібліотеки",
            $"Додавання: {item.Title}",
            "CatalogService.Add()",
            SolidPrinciple.L,
            "Liskov Substitution Principle",
            "Book, Newspaper та Almanac однаково використовуються як LibraryItem без перевірок конкретного типу.",
            "public void Add(LibraryItem item)\n{\n    _repository.Add(item);\n}",
            3);
        repository.Add(item);
    }

    public LibraryItem AddRandom()
    {
        var item = factory.CreateRandom();
        Add(item);
        return item;
    }

    public bool Update(LibraryItem item)
    {
        tracer.Add(
            "Каталог бібліотеки",
            $"Редагування: {item.Title}",
            "CatalogService.Update()",
            SolidPrinciple.D,
            "Dependency Inversion Principle",
            "Редагування виконується через ICatalogRepository, тому спосіб збереження можна замінити без зміни сервісу.",
            "public bool Update(LibraryItem item)\n{\n    return _repository.Update(item);\n}",
            3);
        return repository.Update(item);
    }

    public bool Remove(Guid id)
    {
        tracer.Add(
            "Каталог бібліотеки",
            "Видалення об'єкта",
            "CatalogService.Remove()",
            SolidPrinciple.D,
            "Dependency Inversion Principle",
            "CatalogService видаляє видання через абстракцію репозиторію.",
            "public bool Remove(Guid id)\n{\n    return _repository.Remove(id);\n}",
            3);
        return repository.Remove(id);
    }

    public IReadOnlyList<LibraryItem> Search(ILibrarySearchStrategy strategy, string query)
    {
        tracer.Add(
            "Каталог бібліотеки",
            $"Пошук {strategy.Name}",
            "CatalogService.Search()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "Нові правила пошуку додаються реалізаціями ILibrarySearchStrategy, а сервіс каталогу залишається закритим для модифікації.",
            "public IReadOnlyList<LibraryItem> Search(\n    ILibrarySearchStrategy strategy, string query)\n{\n    return Items.Where(x => strategy.Matches(x, query)).ToList();\n}",
            4);
        return Items.Where(item => strategy.Matches(item, query)).ToList();
    }

    public void Seed()
    {
        tracer.Add(
            "Каталог бібліотеки",
            "Тестова ініціалізація",
            "CatalogService.Seed()",
            SolidPrinciple.S,
            "Single Responsibility Principle",
            "CatalogService координує каталог, репозиторій зберігає дані, а сутності описують тільки власний стан.",
            "public void Seed()\n{\n    Add(_factory.CreateRandom());\n    Add(_factory.CreateRandom());\n    Add(_factory.CreateRandom());\n}",
            3);

        if (Items.Count == 0)
        {
            AddRandom();
            AddRandom();
            AddRandom();
        }
    }

    public bool RemoveLast()
    {
        var item = Items.LastOrDefault();
        if (item is null)
        {
            return false;
        }

        tracer.Add(
            "Каталог бібліотеки",
            $"Видалення: {item.Title}",
            "CatalogService.RemoveLast()",
            SolidPrinciple.D,
            "Dependency Inversion Principle",
            "Сервіс видаляє об'єкт через ICatalogRepository і не залежить від способу збереження каталогу.",
            "public bool Remove(Guid id)\n{\n    return _repository.Remove(id);\n}",
            3);
        return repository.Remove(item.Id);
    }
}
