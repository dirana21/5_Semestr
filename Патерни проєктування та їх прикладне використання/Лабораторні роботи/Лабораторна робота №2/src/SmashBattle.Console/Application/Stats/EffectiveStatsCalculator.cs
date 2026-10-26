using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Stats;

public sealed class EffectiveStatsCalculator
{
    private readonly IReadOnlyList<IStatsModifier> _modifiers;

    public EffectiveStatsCalculator(IEnumerable<IStatsModifier> modifiers) => _modifiers = modifiers.ToList();

    public EffectiveStats Calculate(Combatant actor, BattleState battle)
    {
        var stats = new EffectiveStats(
            actor.BaseStats.MaximumHealth,
            actor.BaseStats.MinimumDamage,
            actor.BaseStats.MaximumDamage,
            actor.BaseStats.Defense,
            actor.BaseStats.Speed,
            actor.BaseStats.CriticalChance,
            actor.BaseStats.DodgeChance);
        return _modifiers.Aggregate(stats, (current, modifier) => modifier.Apply(actor, current, battle));
    }
}
