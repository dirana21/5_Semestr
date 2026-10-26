using SmashBattle.Application.Battle;
using SmashBattle.Application.Commands;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Events;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Common;
using SmashBattle.Presentation.Input;
using SmashBattle.Presentation.Rendering;

namespace SmashBattle.Presentation.Controllers;

public sealed class PlayerKeyboardController
{
    private readonly CommandDispatcher _commands;
    private readonly MovementService _movement;
    private readonly CombatService _combat;
    private readonly AbilityService _abilities;
    private readonly BattleSaveController _saves;
    private readonly BattleLogViewer _logViewer;
    private readonly BattleEventPublisher _events;

    public PlayerKeyboardController(CommandDispatcher commands, MovementService movement, CombatService combat,
        AbilityService abilities, BattleSaveController saves, BattleLogViewer logViewer,
        BattleEventPublisher events)
    {
        _commands = commands;
        _movement = movement;
        _combat = combat;
        _abilities = abilities;
        _saves = saves;
        _logViewer = logViewer;
        _events = events;
    }

    public void Handle(BattleSession session, ConsoleKey key, IConsoleInputReader reader)
    {
        switch (key)
        {
            case ConsoleKey.W:
            case ConsoleKey.UpArrow: Move(session, 0, -1); break;
            case ConsoleKey.A:
            case ConsoleKey.LeftArrow: Move(session, -1, 0); break;
            case ConsoleKey.S:
            case ConsoleKey.DownArrow: Move(session, 0, 1); break;
            case ConsoleKey.D:
            case ConsoleKey.RightArrow: Move(session, 1, 0); break;
            case ConsoleKey.Tab: session.CycleEnemyTarget(); break;
            case ConsoleKey.Spacebar: Attack(session); break;
            case ConsoleKey.Q: UseAbility(session); break;
            case ConsoleKey.E: _commands.Dispatch(new EndTurnCommand(session)); break;
            case ConsoleKey.P: session.IsPaused = !session.IsPaused; break;
            case ConsoleKey.L: _logViewer.Show(session.Log, reader); break;
            case ConsoleKey.F5: _saves.Save(session); break;
            case ConsoleKey.F9: _saves.Load(session); break;
            case ConsoleKey.X:
            case ConsoleKey.Backspace: Cancel(session); break;
            case ConsoleKey.Escape:
                if (session.Mode == InteractionMode.Move) session.ExitRequested = true;
                else Cancel(session);
                break;
        }
    }

    private void Move(BattleSession session, int offsetX, int offsetY)
    {
        var current = session.CurrentActor.Position;
        session.Mode = InteractionMode.Move;
        var moved = _commands.Dispatch(
            new MoveCommand(session, _movement, new Position(current.X + offsetX, current.Y + offsetY)));
        if (!moved)
        {
            var reason = session.CurrentActor.HasUsedAction
                ? "Movement blocked: the action was already used. End the turn with E."
                : "Movement blocked: the cell is occupied, impassable, or costs too many movement points.";
            _events.Publish(new StatusEvent(reason));
        }
    }

    private void Attack(BattleSession session)
    {
        if (session.SelectedTarget is null) session.CycleEnemyTarget();
        if (session.SelectedTarget is not null &&
            !_commands.Dispatch(new AttackCommand(session, _combat, session.SelectedTarget)))
        {
            session.Mode = InteractionMode.Attack;
            _events.Publish(new StatusEvent("Attack mode enabled. Select a highlighted enemy with the mouse."));
        }
    }

    private void UseAbility(BattleSession session)
    {
        if (session.SelectedTarget is not null &&
            _commands.Dispatch(new AbilityCommand(session, _abilities, session.SelectedTarget.Position))) return;
        session.Mode = InteractionMode.Ability;
        _events.Publish(new StatusEvent("Ability mode enabled. Select a highlighted target cell with the mouse."));
    }

    private void Cancel(BattleSession session)
    {
        session.Mode = InteractionMode.Move;
        _events.Publish(new StatusEvent("Target selection cancelled."));
    }
}
