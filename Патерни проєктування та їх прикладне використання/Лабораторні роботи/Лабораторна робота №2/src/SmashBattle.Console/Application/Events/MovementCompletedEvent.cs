using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Events;

public sealed record MovementCompletedEvent(Combatant Actor, Position From, Position To, decimal Cost) : IBattleEvent
{
    public string Message => $"{Actor.Name} moved from ({From.X},{From.Y}) to ({To.X},{To.Y}); cost {Cost:0.0}.";
}
