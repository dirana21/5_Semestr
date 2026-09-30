namespace SolidShowcase.Core;

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
