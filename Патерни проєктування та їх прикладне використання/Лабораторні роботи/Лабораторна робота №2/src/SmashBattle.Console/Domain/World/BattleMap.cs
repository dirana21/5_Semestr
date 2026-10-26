using SmashBattle.Domain.Common;

namespace SmashBattle.Domain.World;

public sealed class BattleMap
{
    private readonly TerrainType[,] _terrain;

    public BattleMap(int width, int height, TerrainType[,] terrain)
    {
        Width = width;
        Height = height;
        _terrain = terrain;
    }

    public int Width { get; }
    public int Height { get; }
    public bool Contains(Position position) =>
        position.X >= 0 && position.X < Width && position.Y >= 0 && position.Y < Height;
    public TerrainType TerrainAt(Position position) => _terrain[position.X, position.Y];
}
