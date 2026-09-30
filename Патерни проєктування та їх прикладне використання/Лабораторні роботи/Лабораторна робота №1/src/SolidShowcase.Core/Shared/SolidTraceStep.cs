namespace SolidShowcase.Core;

public sealed record SolidTraceStep(
    int Sequence,
    string Module,
    string Action,
    string Location,
    SolidPrinciple Principle,
    string PrincipleName,
    string Explanation,
    string Code,
    int HighlightedLine);
