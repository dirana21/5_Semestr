namespace SolidShowcase.Core;

public interface ILibrarySearchStrategy
{
    string Name { get; }
    bool Matches(LibraryItem item, string query);
}
