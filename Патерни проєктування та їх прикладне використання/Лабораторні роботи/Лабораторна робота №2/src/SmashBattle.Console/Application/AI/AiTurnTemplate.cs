using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.AI;

public abstract class AiTurnTemplate : IAiController
{
    private readonly MovementService _movement;
    private readonly CombatService _combat;
    private readonly AbilityService _abilities;
    private readonly DefendService _defend;

    protected AiTurnTemplate(MovementService movement, CombatService combat, AbilityService abilities, DefendService defend)
    {
        _movement = movement;
        _combat = combat;
        _abilities = abilities;
        _defend = defend;
    }

    public void TakeTurn(BattleSession session)
    {
        var actor = session.CurrentActor;
        var target = SelectTarget(session, actor);
        if (target is null) return;

        if (ShouldUseAbility(session, actor, target) && _abilities.Use(session.Battle, actor, target.Position)) return;
        if (_combat.Attack(session.Battle, actor, target)) return;

        var destination = SelectDestination(session, actor, target);
        if (destination is not null)
        {
            _movement.Move(actor, destination.Value, session.ReachableArea);
            session.RefreshReachableArea();
        }

        if (_combat.Attack(session.Battle, actor, target)) return;
        if (ShouldUseAbility(session, actor, target)) _abilities.Use(session.Battle, actor, target.Position);
        if (!actor.HasUsedAction) _defend.Defend(actor);
    }

    protected abstract Combatant? SelectTarget(BattleSession session, Combatant actor);

    protected virtual bool ShouldUseAbility(BattleSession session, Combatant actor, Combatant target) =>
        actor.AbilityCooldown == 0 && actor.Position.ChebyshevDistanceTo(target.Position) <= actor.Ability.Range;

    protected virtual Position? SelectDestination(BattleSession session, Combatant actor, Combatant target)
    {
        var candidates = session.ReachableArea.Costs.Keys.Where(position => position != actor.Position).ToList();
        return candidates.Count == 0
            ? null
            : candidates.MinBy(position => ScorePosition(session, actor, target, position));
    }

    protected virtual decimal ScorePosition(BattleSession session, Combatant actor, Combatant target, Position position) =>
        position.ChebyshevDistanceTo(target.Position);
}
