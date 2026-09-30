namespace SolidShowcase.Core;

public sealed class PublisherSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за видавництвом";
    public bool Matches(LibraryItem item, string query) =>
        item.Publisher.Contains(query, StringComparison.OrdinalIgnoreCase);
}
