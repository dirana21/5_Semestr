using SmashBattle.Creation.Clans;
using SmashBattle.Creation.World;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;

namespace SmashBattle.Creation.Battle;

public sealed class BattleBuilder
{
    private readonly MapGenerator _mapGenerator;
    private readonly ClanFactoryProvider _factoryProvider;

    public BattleBuilder(MapGenerator mapGenerator, ClanFactoryProvider factoryProvider)
    {
        _mapGenerator = mapGenerator;
        _factoryProvider = factoryProvider;
    }

    public BattleState Build(ClanType playerClan, int seed)
    {
        const int width = 50;
        const int height = 50;
        var map = _mapGenerator.Generate(width, height);
        var clans = new[]
        {
            _factoryProvider.Get(ClanType.Elfis).Create(SpawnBlock(2, 2)),
            _factoryProvider.Get(ClanType.Dwargon).Create(SpawnBlock(width - 7, 2)),
            _factoryProvider.Get(ClanType.Wrumper).Create(SpawnBlock(width / 2 - 2, height - 7))
        };

        var registry = ClanLeadershipRegistry.Instance;
        registry.Clear();
        foreach (var clan in clans) registry.Register(clan);
        return new BattleState(map, clans, playerClan, seed);
    }

    private static IReadOnlyList<Position> SpawnBlock(int startX, int startY) =>
        Enumerable.Range(0, 9)
            .Select(index => new Position(startX + index % 3, startY + index / 3))
            .ToList();
}
