using SmashBattle.Application.Combat;
using SmashBattle.Creation.Combatants;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;
using SmashBattle.Infrastructure.Randomness;

namespace SmashBattle.Tests.Combat;

public sealed class DamagePipelineTests
{
    [Fact]
    public void Calculate_NeverReturnsLessThanOneDamage()
    {
        var catalog = new CombatantPrototypeCatalog();
        var attacker = catalog.Get(ClanType.Wrumper).Clone("Attacker", new WeaponDefinition("Stick", 1, 0),
            new Position(0, 0), false, 1);
        var defender = catalog.Get(ClanType.Dwargon).Clone("Defender", new WeaponDefinition("Shield", 1, 0),
            new Position(1, 0), false, 1);
        var attackStats = new EffectiveStats(100, 1, 1, 0, 1, 0, 0);
        var defenseStats = new EffectiveStats(100, 1, 1, 100, 1, 0, 0);
        var random = new SeededRandomSource(1);
        var pipeline = new DamagePipeline(new RollDamageStage(random), new CriticalDamageStage(random),
            new DefenseDamageStage(), new MinimumDamageStage());

        var result = pipeline.Calculate(new DamageContext(attacker, defender, attackStats, defenseStats));

        Assert.Equal(1, result.Damage);
    }
}
