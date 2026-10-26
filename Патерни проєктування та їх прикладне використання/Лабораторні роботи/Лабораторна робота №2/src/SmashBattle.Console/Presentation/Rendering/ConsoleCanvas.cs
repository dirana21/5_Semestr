namespace SmashBattle.Presentation.Rendering;

public static class ConsoleCanvas
{
    public static string Fit(string text, int width) => text.Length > width
        ? text[..(width - 1)] + "…"
        : text.PadRight(width);

    public static void DrawButton(ScreenRegion region, string label, bool active) =>
        WriteAt(region.Left, region.Top, label.PadRight(region.Width), ConsoleColor.White,
            active ? ConsoleColor.DarkCyan : ConsoleColor.DarkBlue);

    public static void WriteCell(int left, int top, char value, ConsoleColor foreground, ConsoleColor background)
    {
        Console.SetCursorPosition(left, top);
        Console.ForegroundColor = foreground;
        Console.BackgroundColor = background;
        Console.Write(value);
    }

    public static void WriteAt(int left, int top, string value, ConsoleColor foreground = ConsoleColor.Gray,
        ConsoleColor background = ConsoleColor.Black)
    {
        Console.SetCursorPosition(left, top);
        Console.ForegroundColor = foreground;
        Console.BackgroundColor = background;
        Console.Write(value);
    }
}
