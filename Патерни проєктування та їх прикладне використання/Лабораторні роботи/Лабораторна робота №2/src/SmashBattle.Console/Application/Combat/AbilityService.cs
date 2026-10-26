using SmashBattle.Application.Events;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.Common;

namespace SmashBattle.Application.Combat;

public sealed class AbilityService
{
    private readonly CombatService _combat;
    private readonly BattleEventPublisher _events;

    public AbilityService(CombatService combat, BattleEventPublisher events)
    {
        _combat = combat;
        _events = events;
    }

    public bool Use(BattleState battle, Combatant actor, Position center)
    {
        if (actor.HasUsedAction || actor.AbilityCooldown > 0 ||
            actor.Position.ChebyshevDistanceTo(center) > actor.Ability.Range) return false;

        var radius = actor.Ability.AreaRadius;
        var targets = battle.LivingCombatants
            .Where(target => target.Clan != actor.Clan && target.Position.ChebyshevDistanceTo(center) <= radius)
            .ToList();
        if (targets.Count == 0) return false;

        var stun = actor.Clan == ClanType.Dwargon;
        foreach (var target in targets) _combat.ApplyAbilityHit(battle, actor, target, actor.Ability.Name, stun);
        actor.SpendAction(CombatantState.Attacking);
        actor.StartAbilityCooldown();
        _events.Publish(new StatusEvent($"{actor.Name} used {actor.Ability.Name} on {targets.Count} target(s)."));
        return true;
    }
}
