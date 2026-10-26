using SmashBattle.Application.Setup;
using SmashBattle.Application.Randomness;
using SmashBattle.Domain.Clans;

namespace SmashBattle.Presentation.Menus;

public sealed class BattleSetupReader
{
    private readonly ISeedGenerator _seedGenerator;

    public BattleSetupReader(ISeedGenerator seedGenerator) => _seedGenerator = seedGenerator;

    public BattleSetup Read()
    {
        Console.Clear();
        Console.WriteLine("CHOOSE YOUR CLAN");
        Console.WriteLine("1 - Elfis (fast ranged fighters)");
        Console.WriteLine("2 - Dwargon (durable defenders)");
        Console.WriteLine("3 - Wrumper (aggressive warriors)");
        var clan = ReadClan();
        Console.Write("Enter an integer seed or press Enter for a random seed: ");
        var seed = ReadSeed();
        Console.WriteLine($"Battle seed: {seed}");
        return new BattleSetup(clan, seed);
    }

    private int ReadSeed()
    {
        while (true)
        {
            var value = Console.ReadLine()?.Trim();
            if (string.IsNullOrEmpty(value)) return _seedGenerator.Create();
            if (int.TryParse(value, out var seed)) return seed;
            Console.Write("Invalid seed. Enter an integer or leave empty: ");
        }
    }

    private static ClanType ReadClan()
    {
        while (true)
        {
            Console.Write("Clan: ");
            switch (Console.ReadLine()?.Trim())
            {
                case "1": return ClanType.Elfis;
                case "2": return ClanType.Dwargon;
                case "3": return ClanType.Wrumper;
                default: Console.WriteLine("Choose 1, 2 or 3."); break;
            }
        }
    }
}
