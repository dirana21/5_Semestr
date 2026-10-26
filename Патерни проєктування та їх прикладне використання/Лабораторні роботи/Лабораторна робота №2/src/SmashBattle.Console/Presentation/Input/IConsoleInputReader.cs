namespace SmashBattle.Presentation.Input;

public interface IConsoleInputReader : IDisposable
{
    GameInput Read();
}
