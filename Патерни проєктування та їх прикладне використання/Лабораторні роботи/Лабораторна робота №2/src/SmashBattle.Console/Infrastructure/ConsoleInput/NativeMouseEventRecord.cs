using System.Runtime.InteropServices;

namespace SmashBattle.Infrastructure.ConsoleInput;

[StructLayout(LayoutKind.Sequential)]
internal struct NativeMouseEventRecord
{
    public NativeCoord MousePosition;
    public uint ButtonState;
    public uint ControlKeyState;
    public uint EventFlags;
}
