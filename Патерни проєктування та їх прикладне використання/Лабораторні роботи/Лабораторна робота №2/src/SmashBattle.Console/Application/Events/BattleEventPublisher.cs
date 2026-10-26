namespace SmashBattle.Application.Events;

public sealed class BattleEventPublisher
{
    private readonly IReadOnlyList<IBattleEventSubscriber> _subscribers;

    public BattleEventPublisher(IEnumerable<IBattleEventSubscriber> subscribers) =>
        _subscribers = subscribers.ToList();

    public void Publish(IBattleEvent battleEvent)
    {
        foreach (var subscriber in _subscribers) subscriber.Handle(battleEvent);
    }
}
