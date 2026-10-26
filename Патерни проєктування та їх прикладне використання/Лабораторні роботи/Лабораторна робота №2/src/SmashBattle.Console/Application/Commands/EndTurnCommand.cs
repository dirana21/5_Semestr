using SmashBattle.Application.Battle;
using SmashBattle.Application.Turns;

namespace SmashBattle.Application.Commands;

public sealed class EndTurnCommand : IPlayerCommand
{
    private readonly BattleSession _session;

    public EndTurnCommand(BattleSession session) => _session = session;

    public bool Execute()
    {
        _session.Turns.EndTurn(_session.Battle);
        _session.Mode = InteractionMode.Move;
        _session.RefreshReachableArea();
        return true;
    }
}
