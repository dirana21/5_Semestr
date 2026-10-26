using SmashBattle.Domain.Abilities;
using SmashBattle.Domain.Auras;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Creation.Combatants;

public sealed class CombatantPrototypeCatalog
{
    private readonly IReadOnlyDictionary<ClanType, CombatantPrototype> _prototypes =
        new Dictionary<ClanType, CombatantPrototype>
        {
            [ClanType.Wrumper] = new(
                ClanType.Wrumper, 'W', new CombatStats(140, 5, 15, 9, 3m, 0.10m, 0.05m, 8),
                new AbilityDefinition("Whirlwind", 1, 1, 3),
                new AuraDefinition("Rage Aura", 3, 1.20m, 0, 0, 0, 1m)),
            [ClanType.Elfis] = new(
                ClanType.Elfis, 'E', new CombatStats(90, 7, 17, 5, 5m, 0.18m, 0.15m, 12),
                new AbilityDefinition("Arrow Rain", 6, 2, 4),
                new AuraDefinition("Wind Aura", 3, 1m, 0, 2m, 0.10m, 1m)),
            [ClanType.Dwargon] = new(
                ClanType.Dwargon, 'D', new CombatStats(150, 3, 13, 12, 2m, 0.07m, 0.03m, 6),
                new AbilityDefinition("Ground Slam", 1, 1, 4),
                new AuraDefinition("Stone Aura", 3, 1m, 5, 0, 0, 1.15m))
        };

    public CombatantPrototype Get(ClanType clan) => _prototypes[clan];
}
