namespace SolidShowcase.Core;

public interface ITransactionParser
{
    IReadOnlyList<Transaction> Parse(string content);
}
