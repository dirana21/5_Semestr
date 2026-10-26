using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.AI;

public sealed class RangedAiController : AiTurnTemplate
{
    public RangedAiController(MovementService movement, CombatService combat, AbilityService abilities, DefendService defend)
        : base(movement, combat, abilities, defend) { }

    protected override Combatant? SelectTarget(BattleSession session, Combatant actor) =>
        session.Battle.LivingCombatants.Where(target => target.Clan != actor.Clan)
            .OrderBy(target => target.CurrentHealth)
            .ThenBy(target => actor.Position.ChebyshevDistanceTo(target.Position))
            .FirstOrDefault();

    protected override decimal ScorePosition(BattleSession session, Combatant actor, Combatant target, Position position)
    {
        var distance = position.ChebyshevDistanceTo(target.Position);
        var desired = Math.Max(2, actor.Weapon.Range - 1);
        return Math.Abs(distance - desired) + (distance < 2 ? 10 : 0);
    }
}
