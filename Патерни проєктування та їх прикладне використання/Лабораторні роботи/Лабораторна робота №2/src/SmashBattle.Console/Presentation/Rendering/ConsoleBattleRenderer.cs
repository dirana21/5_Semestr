using SmashBattle.Application.Battle;
using SmashBattle.Domain.Common;

namespace SmashBattle.Presentation.Rendering;

public sealed class ConsoleBattleRenderer
{
    private readonly ConsoleMapRenderer _map;
    private readonly ConsoleHudRenderer _hud;
    private readonly ConsoleBattleLogRenderer _log;

    public ConsoleBattleRenderer(ConsoleMapRenderer map, ConsoleHudRenderer hud, ConsoleBattleLogRenderer log)
    {
        _map = map;
        _hud = hud;
        _log = log;
    }

    public void Render(BattleSession session)
    {
        Console.CursorVisible = false;
        Console.Clear();
        if (!HasRequiredSize())
        {
            Console.WriteLine($"Please enlarge the console to at least {ConsoleLayout.RequiredWidth}x{ConsoleLayout.RequiredHeight}.");
            Console.WriteLine($"Current size: {Console.WindowWidth}x{Console.WindowHeight}. Press Esc to return.");
            return;
        }

        var mode = session.IsPaused ? "PAUSED" : session.Mode.ToString().ToUpperInvariant();
        ConsoleCanvas.WriteAt(1, 0,
            $"SMASH BATTLE  |  Round {session.Battle.Round}  |  Seed {session.Battle.Seed}  |  Mode: {mode}",
            ConsoleColor.White);
        ConsoleCanvas.WriteAt(1, 1,
            $"Viewport ({session.CurrentActor.Position.X},{session.CurrentActor.Position.Y})  □ move  white target  ◇ ability  · aura",
            ConsoleColor.DarkGray);
        _map.Render(session);
        _hud.Render(session);
        _log.Render(session.Log);
        Console.ResetColor();
    }

    public Position? ScreenToWorld(int x, int y) => _map.ScreenToWorld(x, y);
    public HudAction HitTest(int x, int y) => _hud.HitTest(x, y);
    public static bool HasRequiredSize() =>
        Console.WindowWidth >= ConsoleLayout.RequiredWidth && Console.WindowHeight >= ConsoleLayout.RequiredHeight;
}
