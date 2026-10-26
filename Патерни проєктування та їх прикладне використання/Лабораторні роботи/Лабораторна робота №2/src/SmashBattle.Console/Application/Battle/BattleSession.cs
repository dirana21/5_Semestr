using SmashBattle.Application.Logging;
using SmashBattle.Application.Movement;
using SmashBattle.Application.Turns;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Battle;

public sealed class BattleSession
{
    private readonly ReachableAreaFinder _reachableAreaFinder;

    public BattleSession(BattleState battle, TurnScheduler turns, BattleLog log, ReachableAreaFinder reachableAreaFinder)
    {
        Battle = battle;
        Turns = turns;
        Log = log;
        _reachableAreaFinder = reachableAreaFinder;
        turns.Start(battle);
        RefreshReachableArea();
    }

    public BattleState Battle { get; }
    public TurnScheduler Turns { get; }
    public BattleLog Log { get; }
    public Combatant CurrentActor => Turns.Current;
    public ReachableArea ReachableArea { get; private set; } = new(new Dictionary<Position, decimal>(), new Dictionary<Position, Position>());
    public InteractionMode Mode { get; set; }
    public bool IsPaused { get; set; }
    public bool ExitRequested { get; set; }
    public bool IsPlayerTurn => CurrentActor.Clan == Battle.PlayerClan;
    public ClanType? Winner { get; set; }
    public string LastInput { get; private set; } = "None";
    public Guid? SelectedTargetId { get; private set; }
    public Combatant? SelectedTarget => Battle.LivingCombatants.FirstOrDefault(actor => actor.Id == SelectedTargetId);

    public void RefreshReachableArea() => ReachableArea = _reachableAreaFinder.Find(Battle, CurrentActor);

    public Combatant? CombatantAt(Position position) => Battle.LivingCombatants.FirstOrDefault(actor => actor.Position == position);

    public void CycleEnemyTarget()
    {
        var enemies = Battle.LivingCombatants.Where(actor => actor.Clan != CurrentActor.Clan)
            .OrderBy(actor => CurrentActor.Position.ChebyshevDistanceTo(actor.Position)).ToList();
        if (enemies.Count == 0) { SelectedTargetId = null; return; }
        var currentIndex = enemies.FindIndex(actor => actor.Id == SelectedTargetId);
        SelectedTargetId = enemies[(currentIndex + 1) % enemies.Count].Id;
    }

    public void SelectTarget(Combatant target) => SelectedTargetId = target.Id;

    public void RecordInput(string input) => LastInput = input;
}
