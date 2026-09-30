using System.Globalization;
using System.Text.Json;

namespace SolidShowcase.Core;

public sealed record Transaction(Guid Id, string Description, decimal Amount);

public sealed record ImportResult(int Total, int Imported, int Rejected, decimal TotalAmount);

public interface IDataReader
{
    string Read();
}

public interface ITransactionParser
{
    IReadOnlyList<Transaction> Parse(string content);
}

public interface ITransactionValidator
{
    bool IsValid(Transaction transaction);
}

public interface ITransactionRepository
{
    void Save(IReadOnlyCollection<Transaction> transactions);
    IReadOnlyList<Transaction> GetAll();
}

public interface IProgressReporter
{
    void ReportProgress(int percentage);
}

public interface IImportSummaryWriter
{
    string WriteSummary(ImportResult result);
}

public sealed class StringDataReader(string content, SolidTracer tracer) : IDataReader
{
    public string Read()
    {
        tracer.Add(
            "Імпорт даних",
            "Зчитування джерела",
            "StringDataReader.Read()",
            SolidPrinciple.L,
            "Liskov Substitution Principle",
            "ImportProcessor працює з IDataReader. Рядкове, файлове або мережеве джерело можна підставити без зміни алгоритму імпорту.",
            "public string Read()\n{\n    return _content;\n}",
            3);
        return content;
    }
}

public sealed class CsvTransactionParser(SolidTracer tracer) : ITransactionParser
{
    public IReadOnlyList<Transaction> Parse(string content)
    {
        tracer.Add(
            "Імпорт даних",
            "Парсинг CSV",
            "CsvTransactionParser.Parse()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "Новий формат додається новим класом ITransactionParser. ImportProcessor при цьому не змінюється.",
            "public IReadOnlyList<Transaction> Parse(string content)\n{\n    return content.Split('\\n')\n        .Skip(1)\n        .Select(ParseRow)\n        .ToList();\n}",
            3);

        return content
            .Split(['\r', '\n'], StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
            .Skip(1)
            .Select(line => line.Split(','))
            .Where(parts => parts.Length == 3)
            .Select(parts => new Transaction(
                Guid.Parse(parts[0]),
                parts[1],
                decimal.Parse(parts[2], CultureInfo.InvariantCulture)))
            .ToList();
    }
}

public sealed class JsonTransactionParser(SolidTracer tracer) : ITransactionParser
{
    public IReadOnlyList<Transaction> Parse(string content)
    {
        tracer.Add(
            "Імпорт даних",
            "Парсинг JSON",
            "JsonTransactionParser.Parse()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "JSON підтримано окремою реалізацією того самого контракту. Для XML або YAML достатньо додати ще один парсер.",
            "public IReadOnlyList<Transaction> Parse(string content)\n{\n    return JsonSerializer\n        .Deserialize<List<Transaction>>(content) ?? [];\n}",
            3);

        return JsonSerializer.Deserialize<List<Transaction>>(content) ?? [];
    }
}

public sealed class PositiveAmountValidator(SolidTracer tracer) : ITransactionValidator
{
    public bool IsValid(Transaction transaction)
    {
        tracer.Add(
            "Імпорт даних",
            $"Валідація: {transaction.Description}",
            "PositiveAmountValidator.IsValid()",
            SolidPrinciple.S,
            "Single Responsibility Principle",
            "Валідатор має одну причину для зміни: змінилися правила перевірки транзакції.",
            "public bool IsValid(Transaction transaction)\n{\n    return transaction.Amount > 0;\n}",
            3);
        return transaction.Amount > 0;
    }
}

public sealed class InMemoryTransactionRepository(SolidTracer tracer) : ITransactionRepository
{
    private readonly List<Transaction> _transactions = [];

    public void Save(IReadOnlyCollection<Transaction> transactions)
    {
        tracer.Add(
            "Імпорт даних",
            "Збереження валідних даних",
            "InMemoryTransactionRepository.Save()",
            SolidPrinciple.S,
            "Single Responsibility Principle",
            "Репозиторій відповідає тільки за збереження. Формат і перевірка даних належать іншим компонентам.",
            "public void Save(IReadOnlyCollection<Transaction> items)\n{\n    _transactions.AddRange(items);\n}",
            3);
        _transactions.AddRange(transactions);
    }

    public IReadOnlyList<Transaction> GetAll() => _transactions;
}

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

public sealed class TextImportSummaryWriter : IImportSummaryWriter
{
    public string WriteSummary(ImportResult result) =>
        $"Оброблено: {result.Total}; імпортовано: {result.Imported}; відхилено: {result.Rejected}; сума: {result.TotalAmount:0.00}";
}

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
