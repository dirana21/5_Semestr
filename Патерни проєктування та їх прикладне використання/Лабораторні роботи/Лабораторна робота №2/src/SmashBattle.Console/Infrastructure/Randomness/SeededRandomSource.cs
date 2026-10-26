using SmashBattle.Application.Randomness;

namespace SmashBattle.Infrastructure.Randomness;

public sealed class SeededRandomSource : IRandomSource
{
    private ulong _state;

    public SeededRandomSource(int seed)
    {
        _state = unchecked((ulong)(long)seed) + 0x9E3779B97F4A7C15UL;
        if (_state == 0) _state = 0xA5A5A5A5A5A5A5A5UL;
    }

    public ulong State => _state;

    public int Next(int minimumInclusive, int maximumExclusive)
    {
        if (minimumInclusive >= maximumExclusive) throw new ArgumentOutOfRangeException(nameof(maximumExclusive));
        var range = (uint)(maximumExclusive - minimumInclusive);
        return minimumInclusive + (int)(NextUInt64() % range);
    }

    public double NextDouble() => (NextUInt64() >> 11) * (1.0 / (1UL << 53));

    public void Restore(ulong state) => _state = state == 0 ? 0xA5A5A5A5A5A5A5A5UL : state;

    private ulong NextUInt64()
    {
        var value = _state;
        value ^= value >> 12;
        value ^= value << 25;
        value ^= value >> 27;
        _state = value;
        return value * 2685821657736338717UL;
    }
}
