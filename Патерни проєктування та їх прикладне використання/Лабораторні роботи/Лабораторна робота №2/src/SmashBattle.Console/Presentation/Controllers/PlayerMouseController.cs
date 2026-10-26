using SmashBattle.Application.Battle;
using SmashBattle.Application.Commands;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Movement;
using SmashBattle.Presentation.Rendering;

namespace SmashBattle.Presentation.Controllers;

public sealed class PlayerMouseController
{
    private readonly CommandDispatcher _commands;
    private readonly MovementService _movement;
    private readonly CombatService _combat;
    private readonly AbilityService _abilities;
    private readonly DefendService _defend;
    private readonly ConsoleBattleRenderer _renderer;

    public PlayerMouseController(CommandDispatcher commands, MovementService movement, CombatService combat,
        AbilityService abilities, DefendService defend, ConsoleBattleRenderer renderer)
    {
        _commands = commands;
        _movement = movement;
        _combat = combat;
        _abilities = abilities;
        _defend = defend;
        _renderer = renderer;
    }

    public void Handle(BattleSession session, int x, int y)
    {
        switch (_renderer.HitTest(x, y))
        {
            case HudAction.Attack: session.Mode = InteractionMode.Attack; return;
            case HudAction.Ability: session.Mode = InteractionMode.Ability; return;
            case HudAction.Defend: _commands.Dispatch(new DefendCommand(session, _defend)); return;
            case HudAction.EndTurn: _commands.Dispatch(new EndTurnCommand(session)); return;
            case HudAction.Cancel: session.Mode = InteractionMode.Move; return;
        }

        var position = _renderer.ScreenToWorld(x, y);
        if (position is null) return;
        var target = session.CombatantAt(position.Value);
        if (target is not null && target.Clan != session.CurrentActor.Clan) session.SelectTarget(target);
        IPlayerCommand command = session.Mode switch
        {
            InteractionMode.Attack when target is not null => new AttackCommand(session, _combat, target),
            InteractionMode.Ability => new AbilityCommand(session, _abilities, position.Value),
            _ => new MoveCommand(session, _movement, position.Value)
        };
        if (_commands.Dispatch(command) && session.Mode != InteractionMode.Move) session.Mode = InteractionMode.Move;
    }
}
