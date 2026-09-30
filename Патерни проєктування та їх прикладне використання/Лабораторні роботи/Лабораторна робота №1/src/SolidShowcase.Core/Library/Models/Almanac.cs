namespace SolidShowcase.Core;

public sealed record Almanac(Guid Id, string Title, int Year, string Publisher, string Genre, IReadOnlyList<string> Works)
    : LibraryItem(Id, Title, Year, Publisher)
{
    public override string Kind => "Альманах";
    public override string Details => $"{Genre}; твори: {string.Join(", ", Works)}";
}
