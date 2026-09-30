namespace SolidShowcase.Core;

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
