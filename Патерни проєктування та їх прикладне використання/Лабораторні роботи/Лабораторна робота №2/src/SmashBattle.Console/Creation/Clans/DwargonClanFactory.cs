using SmashBattle.Application.Randomness;
using SmashBattle.Creation.Combatants;
using SmashBattle.Creation.Equipment;
using SmashBattle.Creation.Names;
using SmashBattle.Domain.Clans;

namespace SmashBattle.Creation.Clans;

public sealed class DwargonClanFactory : ClanFactoryBase
{
    private readonly CombatantPrototypeCatalog _prototypes;

    public DwargonClanFactory(CombatantPrototypeCatalog prototypes, INameProvider names, WeaponCatalog weapons,
        IRandomSource random) : base(names, weapons, random) => _prototypes = prototypes;

    public override ClanType ClanType => ClanType.Dwargon;
    protected override CombatantPrototype CreatePrototype() => _prototypes.Get(ClanType);
}
