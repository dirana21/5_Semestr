using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Combat;

public sealed class DamageContext
{
    public DamageContext(Combatant attacker, Combatant defender, EffectiveStats attackerStats, EffectiveStats defenderStats)
    {
        Attacker = attacker;
        Defender = defender;
        AttackerStats = attackerStats;
        DefenderStats = defenderStats;
    }

    public Combatant Attacker { get; }
    public Combatant Defender { get; }
    public EffectiveStats AttackerStats { get; }
    public EffectiveStats DefenderStats { get; }
    public int Damage { get; set; }
    public bool IsCritical { get; set; }
}
