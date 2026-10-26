using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Stats;

public interface IStatsModifier
{
    EffectiveStats Apply(Combatant actor, EffectiveStats current, BattleState battle);
}
