using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Equipment;

namespace SmashBattle.Creation.Equipment;

public sealed class WeaponCatalog
{
    private readonly IReadOnlyDictionary<ClanType, IReadOnlyList<WeaponDefinition>> _weapons =
        new Dictionary<ClanType, IReadOnlyList<WeaponDefinition>>
        {
            [ClanType.Wrumper] =
            [
                new("Battle Axe", 1, 2), new("Mace", 1, 1), new("Morning Star", 1, 2),
                new("Great Axe", 1, 3), new("Hand Axe", 1, 1), new("Mace and Shield", 1, 0),
                new("Greatsword", 1, 3), new("Halberd", 2, 2)
            ],
            [ClanType.Elfis] =
            [
                new("Longbow", 6, 1), new("Elven Sword", 1, 2), new("Arcane Staff", 5, 2)
            ],
            [ClanType.Dwargon] =
            [
                new("War Hammer", 1, 2), new("Hammer and Shield", 1, 0),
                new("Great Hammer", 1, 3), new("Dwarven Axe", 1, 2), new("War Pick", 1, 1)
            ]
        };

    public IReadOnlyList<WeaponDefinition> For(ClanType clan) => _weapons[clan];
}
