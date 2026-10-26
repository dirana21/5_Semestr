using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.AI;

public sealed class AggressiveAiController : AiTurnTemplate
{
    public AggressiveAiController(MovementService movement, CombatService combat, AbilityService abilities, DefendService defend)
        : base(movement, combat, abilities, defend) { }

    protected override Combatant? SelectTarget(BattleSession session, Combatant actor) =>
        session.Battle.LivingCombatants.Where(target => target.Clan != actor.Clan)
            .MinBy(target => actor.Position.ChebyshevDistanceTo(target.Position));
}
