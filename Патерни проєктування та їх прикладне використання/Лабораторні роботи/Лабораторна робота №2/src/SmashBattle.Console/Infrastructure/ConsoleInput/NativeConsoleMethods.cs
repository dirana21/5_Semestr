using System.Runtime.InteropServices;

namespace SmashBattle.Infrastructure.ConsoleInput;

internal static class NativeConsoleMethods
{
    [DllImport("kernel32.dll", SetLastError = true)]
    internal static extern nint GetStdHandle(int standardHandle);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool GetConsoleMode(nint consoleHandle, out uint mode);

    [DllImport("kernel32.dll", SetLastError = true)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool SetConsoleMode(nint consoleHandle, uint mode);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool PeekConsoleInputW(
        nint consoleHandle,
        [Out] NativeInputRecord[] records,
        uint length,
        out uint recordsRead);

    [DllImport("kernel32.dll", SetLastError = true, CharSet = CharSet.Unicode)]
    [return: MarshalAs(UnmanagedType.Bool)]
    internal static extern bool ReadConsoleInputW(
        nint consoleHandle,
        [Out] NativeInputRecord[] records,
        uint length,
        out uint recordsRead);
}
