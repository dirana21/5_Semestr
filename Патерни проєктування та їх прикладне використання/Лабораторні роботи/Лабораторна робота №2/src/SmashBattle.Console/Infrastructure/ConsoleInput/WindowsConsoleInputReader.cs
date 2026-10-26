using SmashBattle.Presentation.Input;

namespace SmashBattle.Infrastructure.ConsoleInput;

public sealed class WindowsConsoleInputReader : IConsoleInputReader
{
    private const int StandardInputHandle = -10;
    private const ushort KeyEvent = 0x0001;
    private const ushort MouseEvent = 0x0002;
    private const uint LeftButton = 0x0001;
    private const uint RightButton = 0x0002;
    private const uint EnableProcessedInput = 0x0001;
    private const uint EnableMouseInput = 0x0010;
    private const uint EnableWindowInput = 0x0008;
    private const uint EnableQuickEditMode = 0x0040;
    private const uint EnableExtendedFlags = 0x0080;
    private const uint EnableVirtualTerminalInput = 0x0200;

    private readonly nint _handle;
    private readonly uint _originalMode;
    private bool _disposed;

    public WindowsConsoleInputReader()
    {
        _handle = NativeConsoleMethods.GetStdHandle(StandardInputHandle);
        if (!NativeConsoleMethods.GetConsoleMode(_handle, out _originalMode))
            throw new InvalidOperationException("The application requires an interactive Windows console.");
        var mode = (_originalMode | EnableProcessedInput | EnableMouseInput | EnableWindowInput | EnableExtendedFlags) &
                   ~(EnableQuickEditMode | EnableVirtualTerminalInput);
        NativeConsoleMethods.SetConsoleMode(_handle, mode);
    }

    public GameInput Read()
    {
        var records = new NativeInputRecord[1];
        while (true)
        {
            if (!NativeConsoleMethods.PeekConsoleInputW(_handle, records, 1, out var available) || available == 0)
            {
                Thread.Sleep(5);
                continue;
            }

            if (records[0].EventType == KeyEvent)
            {
                var key = Console.ReadKey(true);
                return new GameInput(GameInputType.Key, key.Key);
            }

            if (!NativeConsoleMethods.ReadConsoleInputW(_handle, records, 1, out var count) || count == 0) continue;
            var input = records[0];
            if (input.EventType == MouseEvent && input.MouseEvent.EventFlags == 0 &&
                (input.MouseEvent.ButtonState & LeftButton) != 0)
                return new GameInput(GameInputType.LeftClick, X: input.MouseEvent.MousePosition.X,
                    Y: input.MouseEvent.MousePosition.Y);
            if (input.EventType == MouseEvent && input.MouseEvent.EventFlags == 0 &&
                (input.MouseEvent.ButtonState & RightButton) != 0)
                return new GameInput(GameInputType.RightClick, X: input.MouseEvent.MousePosition.X,
                    Y: input.MouseEvent.MousePosition.Y);
        }
    }

    public void Dispose()
    {
        if (_disposed) return;
        NativeConsoleMethods.SetConsoleMode(_handle, _originalMode);
        _disposed = true;
    }
}
