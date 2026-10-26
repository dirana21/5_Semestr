using SmashBattle.Application.Battle;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Commands;

public sealed class MoveCommand : IPlayerCommand
{
    private readonly BattleSession _session;
    private readonly MovementService _movement;
    private readonly Position _destination;

    public MoveCommand(BattleSession session, MovementService movement, Position destination)
    {
        _session = session;
        _movement = movement;
        _destination = destination;
    }

    public bool Execute()
    {
        var moved = _movement.Move(_session.CurrentActor, _destination, _session.ReachableArea);
        if (moved) _session.RefreshReachableArea();
        return moved;
    }
}
