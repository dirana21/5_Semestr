namespace SolidShowcase.Core;

public sealed record Newspaper(Guid Id, string Title, int Year, string Publisher, int IssueNumber, DateOnly ReleaseDate, string Columns)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Газета";
    public override string Details => $"№{IssueNumber}, {ReleaseDate:dd.MM.yyyy}; {Columns}";
}
