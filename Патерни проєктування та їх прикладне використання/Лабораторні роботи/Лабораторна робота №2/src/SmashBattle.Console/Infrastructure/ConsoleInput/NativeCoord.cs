using System.Runtime.InteropServices;

namespace SmashBattle.Infrastructure.ConsoleInput;

[StructLayout(LayoutKind.Sequential)]
internal struct NativeCoord
{
    public short X;
    public short Y;
}
