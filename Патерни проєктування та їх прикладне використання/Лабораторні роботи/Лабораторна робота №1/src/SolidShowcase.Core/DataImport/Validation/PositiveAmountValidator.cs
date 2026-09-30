namespace SolidShowcase.Core;

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
