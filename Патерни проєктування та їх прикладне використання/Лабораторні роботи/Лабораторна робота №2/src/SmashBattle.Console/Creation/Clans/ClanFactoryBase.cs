using SmashBattle.Application.Randomness;
using SmashBattle.Creation.Combatants;
using SmashBattle.Creation.Equipment;
using SmashBattle.Creation.Names;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;

namespace SmashBattle.Creation.Clans;

public abstract class ClanFactoryBase : IClanFactory
{
    private readonly INameProvider _names;
    private readonly WeaponCatalog _weapons;
    private readonly IRandomSource _random;

    protected ClanFactoryBase(INameProvider names, WeaponCatalog weapons, IRandomSource random)
    {
        _names = names;
        _weapons = weapons;
        _random = random;
    }

    public abstract ClanType ClanType { get; }

    public Clan Create(IReadOnlyList<Position> spawnPositions)
    {
        var prototype = CreatePrototype();
        var count = _random.Next(3, 6);
        var leaderIndex = _random.Next(0, count);
        var weaponPool = _weapons.For(ClanType);
        var members = Enumerable.Range(0, count).Select(index => prototype.Clone(
            _names.Next(ClanType),
            weaponPool[_random.Next(0, weaponPool.Count)],
            spawnPositions[index],
            index == leaderIndex,
            _random.Next(1, 7))).ToList();
        return new Clan(ClanType, members);
    }

    protected abstract CombatantPrototype CreatePrototype();
}
