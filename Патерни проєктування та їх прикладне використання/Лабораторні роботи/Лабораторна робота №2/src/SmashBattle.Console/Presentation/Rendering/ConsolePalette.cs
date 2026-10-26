using SmashBattle.Domain.Clans;
using SmashBattle.Domain.World;

namespace SmashBattle.Presentation.Rendering;

public static class ConsolePalette
{
    public static ConsoleColor ForClan(ClanType clan) => clan switch
    {
        ClanType.Elfis => ConsoleColor.Green,
        ClanType.Dwargon => ConsoleColor.Yellow,
        ClanType.Wrumper => ConsoleColor.Red,
        _ => ConsoleColor.Black
    };

    public static ConsoleColor ForTerrain(TerrainType terrain) => terrain switch
    {
        TerrainType.Forest => ConsoleColor.DarkGreen,
        TerrainType.Rocks => ConsoleColor.DarkGray,
        TerrainType.Water => ConsoleColor.Blue,
        TerrainType.Hill => ConsoleColor.DarkYellow,
        _ => ConsoleColor.Gray
    };
}
