using SmashBattle.Application.AI;
using SmashBattle.Application.Auras;
using SmashBattle.Application.Events;
using SmashBattle.Application.Turns;
using SmashBattle.Domain.Combatants;
using SmashBattle.Infrastructure.ConsoleInput;
using SmashBattle.Presentation.Controllers;
using SmashBattle.Presentation.Input;
using SmashBattle.Presentation.Rendering;

namespace SmashBattle.Application.Battle;

public sealed class BattleLoop
{
    private readonly ConsoleBattleRenderer _renderer;
    private readonly PlayerTurnController _player;
    private readonly AiControllerProvider _ai;
    private readonly VictoryCondition _victory;
    private readonly BattleEventPublisher _events;
    private readonly AuraService _auras;

    public BattleLoop(ConsoleBattleRenderer renderer, PlayerTurnController player, AiControllerProvider ai,
        VictoryCondition victory, BattleEventPublisher events, AuraService auras)
    {
        _renderer = renderer;
        _player = player;
        _ai = ai;
        _victory = victory;
        _events = events;
        _auras = auras;
    }

    public void Run(BattleSession session)
    {
        using var input = new WindowsConsoleInputReader();
        while (!session.ExitRequested && session.Winner is null)
        {
            _auras.Refresh(session.Battle);
            _renderer.Render(session);
            if (!ConsoleBattleRenderer.HasRequiredSize())
            {
                var resizeInput = input.Read();
                if (resizeInput.Type == GameInputType.Key && resizeInput.Key == ConsoleKey.Escape)
                    session.ExitRequested = true;
                continue;
            }

            if (session.IsPaused)
            {
                var pauseInput = input.Read();
                if (pauseInput.Type == GameInputType.Key && pauseInput.Key == ConsoleKey.P)
                    session.IsPaused = false;
                else if (pauseInput.Type == GameInputType.Key && pauseInput.Key == ConsoleKey.Escape)
                    session.ExitRequested = true;
                continue;
            }

            if (session.CurrentActor.State == CombatantState.Stunned)
            {
                _events.Publish(new StatusEvent($"{session.CurrentActor.Name} is stunned and misses the turn."));
                session.Turns.EndTurn(session.Battle);
                session.RefreshReachableArea();
                continue;
            }

            if (session.IsPlayerTurn)
                _player.Handle(session, input.Read(), input);
            else
            {
                _ai.Get(session.CurrentActor.Clan).TakeTurn(session);
                Thread.Sleep(100);
                session.Turns.EndTurn(session.Battle);
                session.RefreshReachableArea();
            }

            session.Winner = _victory.GetWinner(session.Battle);
        }

        _renderer.Render(session);
        Console.CursorVisible = true;
        Console.SetCursorPosition(0, Math.Min(Console.WindowHeight - 1, 30));
        Console.ResetColor();
        Console.WriteLine(session.Winner is null
            ? "Battle closed. Press Enter to return to the menu."
            : $"{session.Winner} wins the battle! Press Enter to return to the menu.");
        Console.ReadLine();
    }
}
