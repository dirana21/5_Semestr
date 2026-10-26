using SmashBattle.Application.Events;

namespace SmashBattle.Application.Logging;

public sealed class BattleLog : IBattleEventSubscriber
{
    private readonly List<BattleLogEntry> _entries = [];

    public IReadOnlyList<BattleLogEntry> Entries => _entries;
    public IReadOnlyList<BattleLogEntry> Latest(int count) => _entries.TakeLast(count).ToList();
    public void Handle(IBattleEvent battleEvent) => _entries.Add(new BattleLogEntry(DateTime.Now, battleEvent.Message));
    public void Clear() => _entries.Clear();
}
