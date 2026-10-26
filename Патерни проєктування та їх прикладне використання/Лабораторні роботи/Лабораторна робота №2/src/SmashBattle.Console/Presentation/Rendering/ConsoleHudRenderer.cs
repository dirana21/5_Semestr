using SmashBattle.Application.Battle;
using SmashBattle.Application.Stats;

namespace SmashBattle.Presentation.Rendering;

public sealed class ConsoleHudRenderer
{
    private readonly EffectiveStatsCalculator _stats;

    public ConsoleHudRenderer(EffectiveStatsCalculator stats) => _stats = stats;

    public void Render(BattleSession session)
    {
        var actor = session.CurrentActor;
        var stats = _stats.Calculate(actor, session.Battle);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 2, "┌──────────── CURRENT TURN ────────────┐", ConsoleColor.Cyan);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 3,
            ConsoleCanvas.Fit($"│ Character: {actor.Name}{(actor.IsLeader ? " [LEADER]" : "")}", 43) + "│",
            ConsolePalette.ForClan(actor.Clan));
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 4, ConsoleCanvas.Fit($"│ Clan: {actor.Clan}", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 5, ConsoleCanvas.Fit($"│ HP: {actor.CurrentHealth}/{stats.MaximumHealth}", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 6,
            ConsoleCanvas.Fit($"│ Movement: {actor.MovementPoints:0.0}  Speed: {stats.Speed:0.0}", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 7,
            ConsoleCanvas.Fit($"│ Weapon: {actor.Weapon.Name} (range {actor.Weapon.Range})", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 8,
            ConsoleCanvas.Fit($"│ Action: {(actor.HasUsedAction ? "Used" : "Available")}", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 9,
            ConsoleCanvas.Fit($"│ Ability CD: {actor.AbilityCooldown} | Target: {session.SelectedTarget?.Name ?? "none"}", 43) + "│");
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 10,
            ConsoleCanvas.Fit($"│ Last input: {session.LastInput}", 43) + "│", ConsoleColor.DarkGray);
        ConsoleCanvas.DrawButton(ConsoleLayout.AttackButton, "[ ATTACK ]", session.Mode == InteractionMode.Attack);
        ConsoleCanvas.DrawButton(ConsoleLayout.AbilityButton, "[ ABILITY ]", session.Mode == InteractionMode.Ability);
        ConsoleCanvas.DrawButton(ConsoleLayout.DefendButton, "[ DEFEND ]", false);
        ConsoleCanvas.DrawButton(ConsoleLayout.EndTurnButton, "[ END TURN ]", false);
        ConsoleCanvas.DrawButton(ConsoleLayout.CancelButton, "[ CANCEL ]", false);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 16, "└───────────────────────────────────────────┘", ConsoleColor.Cyan);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 17, "Mouse: cells/buttons | Right click: cancel", ConsoleColor.DarkGray);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 18, "WASD/arrows move | Space attack | Q ability", ConsoleColor.DarkGray);
        ConsoleCanvas.WriteAt(ConsoleLayout.HudLeft, 19, "E end | X cancel | F5/F9 save/load | Esc", ConsoleColor.DarkGray);
    }

    public HudAction HitTest(int x, int y)
    {
        if (ConsoleLayout.AttackButton.Contains(x, y)) return HudAction.Attack;
        if (ConsoleLayout.AbilityButton.Contains(x, y)) return HudAction.Ability;
        if (ConsoleLayout.DefendButton.Contains(x, y)) return HudAction.Defend;
        if (ConsoleLayout.EndTurnButton.Contains(x, y)) return HudAction.EndTurn;
        if (ConsoleLayout.CancelButton.Contains(x, y)) return HudAction.Cancel;
        return HudAction.None;
    }
}
