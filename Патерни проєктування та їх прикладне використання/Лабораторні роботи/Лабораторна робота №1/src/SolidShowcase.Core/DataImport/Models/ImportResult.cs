namespace SolidShowcase.Core;

public sealed record ImportResult(int Total, int Imported, int Rejected, decimal TotalAmount);
