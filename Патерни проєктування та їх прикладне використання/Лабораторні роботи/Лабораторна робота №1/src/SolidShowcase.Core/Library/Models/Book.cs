namespace SolidShowcase.Core;

public sealed record Book(Guid Id, string Title, int Year, string Publisher, string Author, string Genre, int Pages)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Книга";
    public override string Details => $"{Author}, {Genre}, {Pages} стор.";
}
