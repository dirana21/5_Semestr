namespace SolidShowcase.Core;

public sealed record Transaction(Guid Id, string Description, decimal Amount);
