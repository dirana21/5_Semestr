namespace SolidShowcase.Core;

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
