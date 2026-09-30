namespace SolidShowcase.Core;

public interface ICatalogRepository
{
    IReadOnlyList<LibraryItem> GetAll();
    void Add(LibraryItem item);
    bool Update(LibraryItem item);
    bool Remove(Guid id);
}
