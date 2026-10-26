using SmashBattle.Application.Events;
using SmashBattle.Application.Stats;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Turns;

public sealed class TurnScheduler
{
    private readonly EffectiveStatsCalculator _stats;
    private readonly BattleEventPublisher _events;
    private List<Combatant> _order = [];

    public TurnScheduler(EffectiveStatsCalculator stats, BattleEventPublisher events)
    {
        _stats = stats;
        _events = events;
    }

    public Combatant Current => _order[CurrentIndex];
    public int CurrentIndex { get; private set; }
    public IReadOnlyList<Combatant> Order => _order;

    public void Start(BattleState battle)
    {
        _order = battle.Clans.SelectMany(clan => clan.Members)
            .OrderByDescending(actor => actor.BaseStats.Initiative)
            .ThenByDescending(actor => actor.BaseStats.Speed)
            .ThenByDescending(actor => actor.CurrentHealth)
            .ThenBy(actor => actor.Name)
            .ToList();
        CurrentIndex = 0;
        BeginCurrent(battle);
    }

    public void EndTurn(BattleState battle)
    {
        do
        {
            CurrentIndex++;
            if (CurrentIndex >= _order.Count)
            {
                CurrentIndex = 0;
                battle.Round++;
            }
        } while (!_order[CurrentIndex].IsAlive);

        battle.TurnIndex = CurrentIndex;
        BeginCurrent(battle);
    }

    public void Restore(BattleState battle, int turnIndex)
    {
        CurrentIndex = Math.Clamp(turnIndex, 0, _order.Count - 1);
        battle.TurnIndex = CurrentIndex;
    }

    private void BeginCurrent(BattleState battle)
    {
        var actor = Current;
        actor.BeginTurn(_stats.Calculate(actor, battle).Speed);
        _events.Publish(new TurnChangedEvent(battle.Round, actor));
    }
}
