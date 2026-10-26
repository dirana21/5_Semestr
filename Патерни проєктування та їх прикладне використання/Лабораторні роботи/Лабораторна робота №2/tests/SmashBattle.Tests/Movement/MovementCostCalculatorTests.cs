using SmashBattle.Application.Movement;
using SmashBattle.Creation.Combatants;
using SmashBattle.Creation.World;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;
using SmashBattle.Domain.World;

namespace SmashBattle.Tests.Movement;

public sealed class MovementCostCalculatorTests
{
    [Theory]
    [InlineData(ClanType.Wrumper, TerrainType.Plain, 2.0)]
    [InlineData(ClanType.Elfis, TerrainType.Forest, 2.0)]
    [InlineData(ClanType.Dwargon, TerrainType.Rocks, 2.0)]
    [InlineData(ClanType.Elfis, TerrainType.Plain, 2.5)]
    public void GetCost_AppliesTerrainAffinity(ClanType clan, TerrainType terrain, double expected)
    {
        var prototype = new CombatantPrototypeCatalog().Get(clan);
        var actor = prototype.Clone("Test", new WeaponDefinition("Test Weapon", 1, 0), new Position(0, 0), false, 1);
        var calculator = new MovementCostCalculator(new TerrainCatalog());

        var result = calculator.GetCost(actor, terrain);

        Assert.Equal((decimal)expected, result);
    }
}
