using SmashBattle.Domain.Common;

namespace SmashBattle.Presentation.Rendering;

public sealed record Viewport(int Left, int Top, int Width, int Height)
{
    public bool Contains(Position position) => position.X >= Left && position.X < Left + Width &&
                                               position.Y >= Top && position.Y < Top + Height;
}
