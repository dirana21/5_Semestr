using SmashBattle.Infrastructure.Randomness;

namespace SmashBattle.Tests.Infrastructure;

public sealed class SeededRandomSourceTests
{
    [Fact]
    public void Restore_RepeatsTheSameFutureSequence()
    {
        var random = new SeededRandomSource(42);
        _ = random.Next(0, 100);
        var savedState = random.State;
        var expected = Enumerable.Range(0, 5).Select(_ => random.Next(0, 1000)).ToList();

        random.Restore(savedState);
        var actual = Enumerable.Range(0, 5).Select(_ => random.Next(0, 1000)).ToList();

        Assert.Equal(expected, actual);
    }
}
