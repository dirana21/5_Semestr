using SmashBattle.Application.Events;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Combat;

public sealed class DefendService
{
    private readonly BattleEventPublisher _events;

    public DefendService(BattleEventPublisher events) => _events = events;

    public bool Defend(Combatant actor)
    {
        if (actor.HasUsedAction || !actor.IsAlive) return false;
        actor.SpendAction(CombatantState.Defending);
        _events.Publish(new StatusEvent($"{actor.Name} takes a defensive stance (+5 defense)."));
        return true;
    }
}
