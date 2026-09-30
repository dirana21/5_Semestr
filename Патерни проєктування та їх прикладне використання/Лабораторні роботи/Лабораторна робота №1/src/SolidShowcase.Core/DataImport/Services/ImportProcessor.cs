namespace SolidShowcase.Core;

public sealed class ImportProcessor(
    IDataReader reader,
    ITransactionParser parser,
    ITransactionValidator validator,
    ITransactionRepository repository,
    IProgressReporter progressReporter,
    IImportSummaryWriter summaryWriter,
    SolidTracer tracer)
{
    public (ImportResult Result, string Summary) Process()
    {
        tracer.Add(
            "Імпорт даних",
            "Запуск пайплайна",
            "ImportProcessor.Process()",
            SolidPrinciple.D,
            "Dependency Inversion Principle",
            "Оркестратор отримує всі залежності через конструктор і знає лише їхні інтерфейси.",
            "public ImportProcessor(\n    IDataReader reader,\n    ITransactionParser parser,\n    ITransactionValidator validator,\n    ITransactionRepository repository,\n    IProgressReporter progress)\n{ ... }",
            2);

        progressReporter.ReportProgress(10);
        var raw = reader.Read();
        var parsed = parser.Parse(raw);
        progressReporter.ReportProgress(45);
        var valid = parsed.Where(validator.IsValid).ToList();
        repository.Save(valid);
        progressReporter.ReportProgress(100);

        var result = new ImportResult(
            parsed.Count,
            valid.Count,
            parsed.Count - valid.Count,
            valid.Sum(item => item.Amount));

        return (result, summaryWriter.WriteSummary(result));
    }
}
