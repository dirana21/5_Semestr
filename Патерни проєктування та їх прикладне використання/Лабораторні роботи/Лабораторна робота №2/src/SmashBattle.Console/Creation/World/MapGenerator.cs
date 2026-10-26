using SmashBattle.Application.Randomness;
using SmashBattle.Domain.World;

namespace SmashBattle.Creation.World;

public sealed class MapGenerator
{
    private readonly IRandomSource _random;

    public MapGenerator(IRandomSource random) => _random = random;

    public BattleMap Generate(int width, int height)
    {
        var terrain = new TerrainType[width, height];
        for (var y = 0; y < height; y++)
            for (var x = 0; x < width; x++)
            {
                var roll = _random.Next(0, 100);
                terrain[x, y] = roll switch
                {
                    < 62 => TerrainType.Plain,
                    < 76 => TerrainType.Forest,
                    < 87 => TerrainType.Rocks,
                    < 93 => TerrainType.Water,
                    _ => TerrainType.Hill
                };
            }

        ClearSpawnArea(terrain, 2, 2);
        ClearSpawnArea(terrain, width - 7, 2);
        ClearSpawnArea(terrain, width / 2 - 2, height - 7);
        return new BattleMap(width, height, terrain);
    }

    private static void ClearSpawnArea(TerrainType[,] terrain, int startX, int startY)
    {
        for (var y = startY; y < startY + 5; y++)
            for (var x = startX; x < startX + 5; x++)
                terrain[x, y] = TerrainType.Plain;
    }
}
