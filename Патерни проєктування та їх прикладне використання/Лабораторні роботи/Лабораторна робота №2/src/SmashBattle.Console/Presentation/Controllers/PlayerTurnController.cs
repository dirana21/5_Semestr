using SmashBattle.Application.Battle;
using SmashBattle.Presentation.Input;

namespace SmashBattle.Presentation.Controllers;

public sealed class PlayerTurnController
{
    private readonly PlayerMouseController _mouse;
    private readonly PlayerKeyboardController _keyboard;

    public PlayerTurnController(PlayerMouseController mouse, PlayerKeyboardController keyboard)
    {
        _mouse = mouse;
        _keyboard = keyboard;
    }

    public void Handle(BattleSession session, GameInput input, IConsoleInputReader reader)
    {
        session.RecordInput(input.Type == GameInputType.Key ? input.Key.ToString() : input.Type.ToString());
        if (input.Type == GameInputType.LeftClick)
            _mouse.Handle(session, input.X, input.Y);
        else if (input.Type == GameInputType.RightClick)
            session.Mode = InteractionMode.Move;
        else
            _keyboard.Handle(session, input.Key, reader);
    }
}
