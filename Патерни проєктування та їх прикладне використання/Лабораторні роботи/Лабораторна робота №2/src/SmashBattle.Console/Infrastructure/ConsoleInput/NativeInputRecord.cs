using System.Runtime.InteropServices;

namespace SmashBattle.Infrastructure.ConsoleInput;

[StructLayout(LayoutKind.Explicit, CharSet = CharSet.Unicode)]
internal struct NativeInputRecord
{
    [FieldOffset(0)] public ushort EventType;
    [FieldOffset(4)] public NativeKeyEventRecord KeyEvent;
    [FieldOffset(4)] public NativeMouseEventRecord MouseEvent;
}
