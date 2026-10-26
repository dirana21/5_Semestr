using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;

namespace SmashBattle.Application.Commands;

public sealed class DefendCommand : IPlayerCommand
{
    private readonly BattleSession _session;
    private readonly DefendService _defend;

    public DefendCommand(BattleSession session, DefendService defend)
    {
        _session = session;
        _defend = defend;
    }

    public bool Execute() => _defend.Defend(_session.CurrentActor);
}
