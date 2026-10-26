using SmashBattle.Domain.Abilities;
using SmashBattle.Domain.Auras;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;

namespace SmashBattle.Creation.Combatants;

public sealed class CombatantPrototype
{
    public CombatantPrototype(
        ClanType clan,
        char symbol,
        CombatStats stats,
        AbilityDefinition ability,
        AuraDefinition leaderAura)
    {
        Clan = clan;
        Symbol = symbol;
        Stats = stats;
        Ability = ability;
        LeaderAura = leaderAura;
    }

    public ClanType Clan { get; }
    public char Symbol { get; }
    public CombatStats Stats { get; }
    public AbilityDefinition Ability { get; }
    public AuraDefinition LeaderAura { get; }

    public Combatant Clone(string name, WeaponDefinition weapon, Position position, bool isLeader, int initiativeRoll)
    {
        var stats = isLeader
            ? Stats with
            {
                MaximumHealth = (int)Math.Ceiling(Stats.MaximumHealth * 1.5m),
                MinimumDamage = (int)Math.Ceiling(Stats.MinimumDamage * 1.2m),
                MaximumDamage = (int)Math.Ceiling(Stats.MaximumDamage * 1.2m),
                Initiative = Stats.Initiative + initiativeRoll + 2
            }
            : Stats with { Initiative = Stats.Initiative + initiativeRoll };

        return new Combatant(Guid.NewGuid(), name, Clan, Symbol, stats, weapon, Ability, position, isLeader,
            isLeader ? LeaderAura : null);
    }
}
