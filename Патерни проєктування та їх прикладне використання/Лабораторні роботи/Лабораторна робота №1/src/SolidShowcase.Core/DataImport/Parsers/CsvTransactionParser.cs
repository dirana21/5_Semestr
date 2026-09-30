using System.Globalization;

namespace SolidShowcase.Core;

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
