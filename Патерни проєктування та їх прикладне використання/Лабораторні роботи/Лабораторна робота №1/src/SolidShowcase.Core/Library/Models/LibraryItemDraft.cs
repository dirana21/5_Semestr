namespace SolidShowcase.Core;

public sealed record LibraryItemDraft(
    string Kind,
    string Title,
    int Year,
    string Publisher,
    string Author,
    string Genre,
    int Pages,
    int IssueNumber,
    DateOnly ReleaseDate,
    string Details);
