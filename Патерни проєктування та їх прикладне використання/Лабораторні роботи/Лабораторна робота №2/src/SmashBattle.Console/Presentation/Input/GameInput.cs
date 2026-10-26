namespace SmashBattle.Presentation.Input;

public sealed record GameInput(GameInputType Type, ConsoleKey Key = 0, int X = 0, int Y = 0);
