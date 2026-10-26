using SmashBattle.Application.Battle;
using SmashBattle.Application.Combat;
using SmashBattle.Application.Movement;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.AI;

public sealed class DefensiveAiController : AiTurnTemplate
{
    public DefensiveAiController(MovementService movement, CombatService combat, AbilityService abilities, DefendService defend)
        : base(movement, combat, abilities, defend) { }

    protected override Combatant? SelectTarget(BattleSession session, Combatant actor)
    {
        var leader = session.Battle.Clans.Single(clan => clan.Type == actor.Clan).Leader;
        return session.Battle.LivingCombatants.Where(target => target.Clan != actor.Clan)
            .MinBy(target => target.Position.ChebyshevDistanceTo(leader.Position));
    }
}
