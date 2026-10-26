namespace SmashBattle.Domain.World;

public sealed record TerrainDefinition(TerrainType Type, char Symbol, decimal MovementCost, bool IsPassable);
