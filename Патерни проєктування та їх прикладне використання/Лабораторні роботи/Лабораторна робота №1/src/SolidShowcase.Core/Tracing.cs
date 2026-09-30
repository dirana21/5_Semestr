namespace SolidShowcase.Core;

public enum SolidPrinciple
{
    S,
    O,
    L,
    I,
    D
}

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

public sealed class SolidTracer
{
    private readonly List<SolidTraceStep> _steps = [];

    public IReadOnlyList<SolidTraceStep> Steps => _steps;

    public void Clear() => _steps.Clear();

    public void Add(
        string module,
        string action,
        string location,
        SolidPrinciple principle,
        string principleName,
        string explanation,
        string code,
        int highlightedLine = 1)
    {
        _steps.Add(new SolidTraceStep(
            _steps.Count + 1,
            module,
            action,
            location,
            principle,
            principleName,
            explanation,
            code,
            highlightedLine));
    }
}

public sealed record DemoResult(string Title, IReadOnlyList<string> Lines);

public sealed record DemoModule(string Id, string Number, string Title, string Subtitle);

public sealed record DemoAction(string Id, string Label, SolidPrinciple Principle, string Hint);
