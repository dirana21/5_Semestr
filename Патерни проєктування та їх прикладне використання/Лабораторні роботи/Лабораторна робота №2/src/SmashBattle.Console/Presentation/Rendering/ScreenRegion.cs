namespace SmashBattle.Presentation.Rendering;

public sealed record ScreenRegion(int Left, int Top, int Width, int Height)
{
    public bool Contains(int x, int y) => x >= Left && x < Left + Width && y >= Top && y < Top + Height;
}
