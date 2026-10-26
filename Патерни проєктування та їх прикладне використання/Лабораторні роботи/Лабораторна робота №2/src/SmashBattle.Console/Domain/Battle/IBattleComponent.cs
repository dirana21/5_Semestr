using SmashBattle.Domain.Combatants;

namespace SmashBattle.Domain.Battle;

public interface IBattleComponent
{
    IEnumerable<Combatant> GetCombatants();
}
