using SmashBattle.Creation.World;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.World;

namespace SmashBattle.Application.Movement;

public sealed class MovementCostCalculator
{
    private readonly TerrainCatalog _terrain;

    public MovementCostCalculator(TerrainCatalog terrain) => _terrain = terrain;

    public decimal GetCost(Combatant actor, TerrainType terrainType) => (actor.Clan, terrainType) switch
    {
        (ClanType.Wrumper, TerrainType.Plain) => 2.0m,
        (ClanType.Elfis, TerrainType.Forest) => 2.0m,
        (ClanType.Dwargon, TerrainType.Rocks) => 2.0m,
        _ => _terrain.Get(terrainType).MovementCost
    };

    public bool IsPassable(TerrainType terrainType) => _terrain.Get(terrainType).IsPassable;
}
