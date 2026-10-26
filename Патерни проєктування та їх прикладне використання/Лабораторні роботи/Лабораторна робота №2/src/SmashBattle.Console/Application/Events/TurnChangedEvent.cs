using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Events;

public sealed record TurnChangedEvent(int Round, Combatant Actor) : IBattleEvent
{
    public string Message => $"Round {Round}: {Actor.Name} ({Actor.Clan}) begins the turn.";
}
