namespace SolidShowcase.Core;

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
        if (item is null) return false;

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
