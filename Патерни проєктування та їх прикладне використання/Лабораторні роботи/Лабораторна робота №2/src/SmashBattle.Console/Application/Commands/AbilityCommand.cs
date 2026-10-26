using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Commands;

public sealed class AbilityCommand : IPlayerCommand
{
    private readonly BattleSession _session;
    private readonly AbilityService _abilities;
    private readonly Position _center;

    public AbilityCommand(BattleSession session, AbilityService abilities, Position center)
    {
        _session = session;
        _abilities = abilities;
        _center = center;
    }

    public bool Execute() => _abilities.Use(_session.Battle, _session.CurrentActor, _center);
}
