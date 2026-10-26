using SmashBattle.Application.Battle;
using SmashBattle.Application.Events;
using SmashBattle.Application.Persistence;
using SmashBattle.Infrastructure.Persistence;

namespace SmashBattle.Presentation.Controllers;

public sealed class BattleSaveController
{
    private readonly BattleMementoFactory _mementos;
    private readonly BattleSaveStore _store;
    private readonly BattleEventPublisher _events;

    public BattleSaveController(BattleMementoFactory mementos, BattleSaveStore store, BattleEventPublisher events)
    {
        _mementos = mementos;
        _store = store;
        _events = events;
    }

    public void Save(BattleSession session)
    {
        _store.Save(_mementos.Capture(session));
        _events.Publish(new StatusEvent("Battle saved successfully."));
    }

    public void Load(BattleSession session)
    {
        var save = _store.Load();
        if (save is null)
        {
            _events.Publish(new StatusEvent("No saved battle was found."));
            return;
        }
        if (save.Seed != session.Battle.Seed || save.PlayerClan != session.Battle.PlayerClan)
        {
            _events.Publish(new StatusEvent("The save belongs to a different battle seed or player clan."));
            return;
        }
        _mementos.Restore(session, save);
        _events.Publish(new StatusEvent("Battle loaded successfully."));
    }
}
