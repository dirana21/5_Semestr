namespace SmashBattle.Presentation.Rendering;

public static class ConsoleLayout
{
    public const int MapLeft = 1;
    public const int MapTop = 2;
    public const int MapWidth = 50;
    public const int MapHeight = 18;
    public const int HudLeft = 54;
    public const int HudWidth = 44;
    public const int RequiredWidth = 100;
    public const int LogLeft = 1;
    public const int LogTop = 21;
    public const int LogInnerWidth = 96;
    public const int RequiredHeight = 32;

    public static ScreenRegion AttackButton { get; } = new(HudLeft + 2, 11, 16, 1);
    public static ScreenRegion AbilityButton { get; } = new(HudLeft + 2, 12, 16, 1);
    public static ScreenRegion DefendButton { get; } = new(HudLeft + 2, 13, 16, 1);
    public static ScreenRegion EndTurnButton { get; } = new(HudLeft + 2, 14, 16, 1);
    public static ScreenRegion CancelButton { get; } = new(HudLeft + 2, 15, 16, 1);
}
