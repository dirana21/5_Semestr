using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Commands;

public sealed class AttackCommand : IPlayerCommand
{
    private readonly BattleSession _session;
    private readonly CombatService _combat;
    private readonly Combatant _target;

    public AttackCommand(BattleSession session, CombatService combat, Combatant target)
    {
        _session = session;
        _combat = combat;
        _target = target;
    }

    public bool Execute() => _combat.Attack(_session.Battle, _session.CurrentActor, _target);
}
