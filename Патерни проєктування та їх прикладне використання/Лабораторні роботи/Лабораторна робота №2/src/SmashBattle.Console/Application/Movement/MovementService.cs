using SmashBattle.Application.Events;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Movement;

public sealed class MovementService
{
    private readonly BattleEventPublisher _events;
    private readonly IMovementStepObserver _stepObserver;

    public MovementService(BattleEventPublisher events, IMovementStepObserver stepObserver)
    {
        _events = events;
        _stepObserver = stepObserver;
    }

    public bool Move(Combatant actor, Position destination, ReachableArea area)
    {
        if (actor.HasUsedAction || !area.Costs.TryGetValue(destination, out var totalCost) || destination == actor.Position)
            return false;
        var origin = actor.Position;
        var path = area.PathTo(destination);
        if (path.Count == 0) return false;

        var previous = origin;
        var previousCumulativeCost = 0m;
        for (var index = 0; index < path.Count; index++)
        {
            var step = path[index];
            var cumulativeCost = area.Costs[step];
            actor.MoveTo(step, cumulativeCost - previousCumulativeCost);
            _stepObserver.OnStep(actor, previous, step, index + 1, path.Count);
            previous = step;
            previousCumulativeCost = cumulativeCost;
        }

        _events.Publish(new MovementCompletedEvent(actor, origin, destination, totalCost));
        return true;
    }
}
