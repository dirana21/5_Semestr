namespace SolidShowcase.Core;

public sealed class MemoryProgressReporter(SolidTracer tracer) : IProgressReporter
{
    public int LastPercentage { get; private set; }

    public void ReportProgress(int percentage)
    {
        LastPercentage = percentage;
        tracer.Add(
            "Імпорт даних",
            $"Прогрес: {percentage}%",
            "MemoryProgressReporter.ReportProgress()",
            SolidPrinciple.I,
            "Interface Segregation Principle",
            "Компонент прогресу реалізує лише вузький IProgressReporter і не залежить від створення підсумкового звіту.",
            "public void ReportProgress(int percentage)\n{\n    LastPercentage = percentage;\n}",
            3);
    }
}
