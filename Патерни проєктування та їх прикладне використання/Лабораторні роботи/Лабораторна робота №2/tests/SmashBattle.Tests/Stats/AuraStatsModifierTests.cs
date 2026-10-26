using SmashBattle.Application.Stats;
using SmashBattle.Creation.Combatants;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;
using SmashBattle.Domain.World;

namespace SmashBattle.Tests.Stats;

public sealed class AuraStatsModifierTests
{
    [Fact]
    public void Apply_BuffsNearbyAllyButNotLeader()
    {
        var prototype = new CombatantPrototypeCatalog().Get(ClanType.Wrumper);
        var weapon = new WeaponDefinition("Axe", 1, 0);
        var leader = prototype.Clone("Leader", weapon, new Position(5, 5), true, 1);
        var ally = prototype.Clone("Ally", weapon, new Position(6, 5), false, 1);
        var terrain = new TerrainType[10, 10];
        var battle = new BattleState(new BattleMap(10, 10, terrain), [new Clan(ClanType.Wrumper, [leader, ally])],
            ClanType.Wrumper, 1);
        var modifier = new AuraStatsModifier();
        var baseStats = new EffectiveStats(140, 5, 15, 9, 3, 0.10m, 0.05m);

        var allyStats = modifier.Apply(ally, baseStats, battle);
        var leaderStats = modifier.Apply(leader, baseStats, battle);

        Assert.Equal(6, allyStats.MinimumDamage);
        Assert.Equal(18, allyStats.MaximumDamage);
        Assert.Equal(baseStats, leaderStats);
    }
}
