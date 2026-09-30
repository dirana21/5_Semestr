namespace SolidShowcase.Core;

public interface ITransactionRepository
{
    void Save(IReadOnlyCollection<Transaction> transactions);
    IReadOnlyList<Transaction> GetAll();
}
