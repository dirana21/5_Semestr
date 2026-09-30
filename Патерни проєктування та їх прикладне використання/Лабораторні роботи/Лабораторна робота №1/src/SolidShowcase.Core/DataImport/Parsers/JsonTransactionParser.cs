using System.Text.Json;

namespace SolidShowcase.Core;

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
