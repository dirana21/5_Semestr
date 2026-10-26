using SmashBattle.Creation.Battle;
using SmashBattle.Creation.Clans;
using SmashBattle.Creation.Combatants;
using SmashBattle.Creation.Equipment;
using SmashBattle.Creation.Names;
using SmashBattle.Creation.World;
using SmashBattle.Domain.Clans;
using SmashBattle.Infrastructure.Randomness;

namespace SmashBattle.Tests.Creation;

public sealed class BattleBuilderTests
{
    [Fact]
    public void Build_CreatesThreeValidClansAndOneLeaderInEach()
    {
        var random = new SeededRandomSource(77);
        var prototypes = new CombatantPrototypeCatalog();
        var names = new GeneratedNameProvider(random);
        var weapons = new WeaponCatalog();
        IClanFactory[] factories =
        [
            new ElfisClanFactory(prototypes, names, weapons, random),
            new DwargonClanFactory(prototypes, names, weapons, random),
            new WrumperClanFactory(prototypes, names, weapons, random)
        ];
        var builder = new BattleBuilder(new MapGenerator(random), new ClanFactoryProvider(factories));

        var battle = builder.Build(ClanType.Elfis, 77);

        Assert.Equal(3, battle.Clans.Count);
        Assert.All(battle.Clans, clan => Assert.InRange(clan.Members.Count, 3, 5));
        Assert.All(battle.Clans, clan => Assert.Single(clan.Members, member => member.IsLeader));
        Assert.Equal(50, battle.Map.Width);
        Assert.Equal(50, battle.Map.Height);
    }
}
