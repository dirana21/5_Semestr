namespace SmashBattle.Application.Randomness;

public interface IRandomSource
{
    ulong State { get; }
    int Next(int minimumInclusive, int maximumExclusive);
    double NextDouble();
    void Restore(ulong state);
}
