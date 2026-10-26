using SmashBattle.Application.Logging;

namespace SmashBattle.Presentation.Rendering;

public sealed class ConsoleBattleLogRenderer
{
    public void Render(BattleLog log)
    {
        var title = " BATTLE LOG — last 8 events ";
        ConsoleCanvas.WriteAt(ConsoleLayout.LogLeft, ConsoleLayout.LogTop,
            "┌" + title.PadRight(ConsoleLayout.LogInnerWidth, '─') + "┐", ConsoleColor.Cyan);
        var entries = log.Latest(8);
        for (var index = 0; index < 8; index++)
        {
            var text = index < entries.Count ? entries[index].Message : string.Empty;
            ConsoleCanvas.WriteAt(ConsoleLayout.LogLeft, ConsoleLayout.LogTop + index + 1,
                "│" + ConsoleCanvas.Fit(" " + text, ConsoleLayout.LogInnerWidth) + "│", ConsoleColor.Gray);
        }
        ConsoleCanvas.WriteAt(ConsoleLayout.LogLeft, ConsoleLayout.LogTop + 9,
            "└" + new string('─', ConsoleLayout.LogInnerWidth) + "┘", ConsoleColor.Cyan);
    }
}
