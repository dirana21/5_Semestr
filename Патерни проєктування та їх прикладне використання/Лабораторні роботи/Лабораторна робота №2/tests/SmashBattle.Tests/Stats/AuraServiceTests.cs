using SmashBattle.Application.Auras;
using SmashBattle.Creation.Combatants;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;
using SmashBattle.Domain.World;

namespace SmashBattle.Tests.Stats;

public sealed class AuraServiceTests
{
    [Fact]
    public void Refresh_RemovesTemporaryMaximumHealthOutsideLeaderRadius()
    {
        var prototype = new CombatantPrototypeCatalog().Get(ClanType.Dwargon);
        var weapon = new WeaponDefinition("Hammer", 1, 0);
        var leader = prototype.Clone("Leader", weapon, new Position(2, 2), true, 1);
        var ally = prototype.Clone("Ally", weapon, new Position(3, 2), false, 1);
        var battle = new BattleState(new BattleMap(10, 10, new TerrainType[10, 10]),
            [new Clan(ClanType.Dwargon, [leader, ally])], ClanType.Dwargon, 1);
        var service = new AuraService();
        service.Initialize(battle);

        Assert.Equal(173, ally.CurrentHealth);
        Assert.Equal(225, leader.CurrentHealth);

        ally.MoveTo(new Position(9, 9), 0);
        service.Refresh(battle);

        Assert.Equal(150, ally.CurrentHealth);
        Assert.Equal(0, ally.TemporaryMaximumHealthBonus);
    }
}
