namespace SolidShowcase.Core;

public sealed class TitleSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за назвою";
    public bool Matches(LibraryItem item, string query) =>
        item.Title.Contains(query, StringComparison.OrdinalIgnoreCase);
}
