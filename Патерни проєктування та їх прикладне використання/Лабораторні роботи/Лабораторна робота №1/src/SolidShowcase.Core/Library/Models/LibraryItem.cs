namespace SolidShowcase.Core;

public abstract record LibraryItem(Guid Id, string Title, int Year, string Publisher)
{
    public abstract string Kind { get; }
    public abstract string Details { get; }
}
