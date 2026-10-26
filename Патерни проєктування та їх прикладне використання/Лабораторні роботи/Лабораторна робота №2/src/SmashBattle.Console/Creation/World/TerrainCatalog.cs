using SmashBattle.Domain.World;

namespace SmashBattle.Creation.World;

public sealed class TerrainCatalog
{
    private readonly IReadOnlyDictionary<TerrainType, TerrainDefinition> _definitions =
        new Dictionary<TerrainType, TerrainDefinition>
        {
            [TerrainType.Plain] = new(TerrainType.Plain, '.', 2.5m, true),
            [TerrainType.Forest] = new(TerrainType.Forest, '♣', 3.5m, true),
            [TerrainType.Rocks] = new(TerrainType.Rocks, '▲', 3.5m, true),
            [TerrainType.Water] = new(TerrainType.Water, '~', decimal.MaxValue, false),
            [TerrainType.Hill] = new(TerrainType.Hill, '^', 3.0m, true)
        };

    public TerrainDefinition Get(TerrainType type) => _definitions[type];
}
