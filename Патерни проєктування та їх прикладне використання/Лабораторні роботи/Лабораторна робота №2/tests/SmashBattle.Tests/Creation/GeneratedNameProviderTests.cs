using SmashBattle.Creation.Names;
using SmashBattle.Domain.Clans;
using SmashBattle.Infrastructure.Randomness;

namespace SmashBattle.Tests.Creation;

public sealed class GeneratedNameProviderTests
{
    [Theory]
    [InlineData(ClanType.Elfis)]
    [InlineData(ClanType.Dwargon)]
    [InlineData(ClanType.Wrumper)]
    public void Next_ProvidesOneHundredUniqueNamesForEachClan(ClanType clan)
    {
        var provider = new GeneratedNameProvider(new SeededRandomSource(12345));

        var names = Enumerable.Range(0, 100).Select(_ => provider.Next(clan)).ToList();

        Assert.Equal(100, names.Distinct().Count());
    }
}
