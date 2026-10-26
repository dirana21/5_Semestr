using SmashBattle.Application.Randomness;
using SmashBattle.Domain.Clans;

namespace SmashBattle.Creation.Names;

public sealed class GeneratedNameProvider : INameProvider
{
    private static readonly string[] ElfPrefixes =
        ["Ael", "Aer", "Cael", "Ela", "Eri", "Fael", "Ili", "Lia", "Syl", "Tha"];
    private static readonly string[] ElfSuffixes =
        ["rion", "wyn", "thas", "riel", "lith", "nor", "drel", "mir", "las", "wen"];
    private static readonly string[] DwarfPrefixes =
        ["Bal", "Brom", "Dor", "Dun", "Far", "Gim", "Kor", "Mor", "Thor", "Ulf"];
    private static readonly string[] DwarfSuffixes =
        ["din", "gar", "grim", "bek", "drum", "rik", "mund", "sten", "rak", "bur"];
    private static readonly string[] WarriorPrefixes =
        ["Ar", "Brand", "Ced", "Drav", "Gar", "Had", "Kor", "Rag", "Tor", "Val"];
    private static readonly string[] WarriorSuffixes =
        ["dor", "ric", "mund", "var", "gan", "rek", "mar", "dan", "grim", "tor"];

    private readonly IRandomSource _random;
    private readonly HashSet<string> _usedNames = [];

    public GeneratedNameProvider(IRandomSource random) => _random = random;

    public string Next(ClanType clan)
    {
        var (prefixes, suffixes) = clan switch
        {
            ClanType.Elfis => (ElfPrefixes, ElfSuffixes),
            ClanType.Dwargon => (DwarfPrefixes, DwarfSuffixes),
            _ => (WarriorPrefixes, WarriorSuffixes)
        };

        for (var attempt = 0; attempt < 100; attempt++)
        {
            var name = prefixes[_random.Next(0, prefixes.Length)] + suffixes[_random.Next(0, suffixes.Length)];
            if (_usedNames.Add(name)) return name;
        }

        return $"{prefixes[0]}{suffixes[0]}-{_usedNames.Count + 1}";
    }
}
