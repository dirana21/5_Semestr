namespace SolidShowcase.Core;

public sealed class AuthorSearchStrategy : ILibrarySearchStrategy
{
    public string Name => "за автором";
    public bool Matches(LibraryItem item, string query) =>
        item is Book book && book.Author.Contains(query, StringComparison.OrdinalIgnoreCase);
}
