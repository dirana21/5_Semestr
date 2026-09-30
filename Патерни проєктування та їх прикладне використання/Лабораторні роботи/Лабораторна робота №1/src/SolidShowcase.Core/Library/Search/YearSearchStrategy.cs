namespace SolidShowcase.Core;

public sealed class YearSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за роком";
    public bool Matches(LibraryItem item, string query) => item.Year.ToString() == query.Trim();
}
