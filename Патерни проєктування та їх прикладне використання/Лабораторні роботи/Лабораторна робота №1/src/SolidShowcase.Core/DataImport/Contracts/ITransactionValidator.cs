namespace SolidShowcase.Core;

public interface ITransactionValidator
{
    bool IsValid(Transaction transaction);
}
