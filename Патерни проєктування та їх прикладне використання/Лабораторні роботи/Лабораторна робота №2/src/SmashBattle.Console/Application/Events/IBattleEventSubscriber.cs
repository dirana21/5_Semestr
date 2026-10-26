namespace SmashBattle.Application.Events;

public interface IBattleEventSubscriber
{
    void Handle(IBattleEvent battleEvent);
}
