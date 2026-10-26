namespace SmashBattle.Application.Events;

public sealed record StatusEvent(string Message) : IBattleEvent;
