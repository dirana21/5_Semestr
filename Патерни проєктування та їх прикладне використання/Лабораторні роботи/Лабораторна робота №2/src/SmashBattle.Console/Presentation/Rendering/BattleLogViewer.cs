using SmashBattle.Application.Logging;
using SmashBattle.Presentation.Input;

namespace SmashBattle.Presentation.Rendering;

public sealed class BattleLogViewer
{
    public void Show(BattleLog log, IConsoleInputReader input)
    {
        var offset = Math.Max(0, log.Entries.Count - Math.Max(1, Console.WindowHeight - 4));
        while (true)
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("FULL BATTLE LOG");
            Console.ForegroundColor = ConsoleColor.DarkGray;
            Console.WriteLine("Up/Down scroll | L or Esc return");
            Console.ForegroundColor = ConsoleColor.Gray;
            var pageSize = Math.Max(1, Console.WindowHeight - 4);
            foreach (var entry in log.Entries.Skip(offset).Take(pageSize))
                Console.WriteLine($"[{entry.CreatedAt:HH:mm:ss}] {entry.Message}");
            var action = input.Read();
            if (action.Type != GameInputType.Key) continue;
            if (action.Key is ConsoleKey.L or ConsoleKey.Escape) return;
            if (action.Key == ConsoleKey.UpArrow) offset = Math.Max(0, offset - 1);
            if (action.Key == ConsoleKey.DownArrow) offset = Math.Min(Math.Max(0, log.Entries.Count - pageSize), offset + 1);
        }
    }
}
