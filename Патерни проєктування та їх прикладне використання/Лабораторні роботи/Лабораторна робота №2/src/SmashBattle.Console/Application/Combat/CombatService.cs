using SmashBattle.Application.Events;
using SmashBattle.Application.Randomness;
using SmashBattle.Application.Stats;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Combat;

public sealed class CombatService
{
    private readonly EffectiveStatsCalculator _stats;
    private readonly DamagePipeline _damage;
    private readonly IRandomSource _random;
    private readonly BattleEventPublisher _events;

    public CombatService(EffectiveStatsCalculator stats, DamagePipeline damage, IRandomSource random, BattleEventPublisher events)
    {
        _stats = stats;
        _damage = damage;
        _random = random;
        _events = events;
    }

    public bool CanAttack(Combatant attacker, Combatant defender) =>
        attacker.IsAlive && defender.IsAlive && attacker.Clan != defender.Clan && !attacker.HasUsedAction &&
        attacker.Position.ChebyshevDistanceTo(defender.Position) <= attacker.Weapon.Range;

    public bool Attack(BattleState battle, Combatant attacker, Combatant defender, string source = "attack")
    {
        if (!CanAttack(attacker, defender)) return false;
        var defenderStats = _stats.Calculate(defender, battle);
        if ((decimal)_random.NextDouble() < defenderStats.DodgeChance)
        {
            attacker.SpendAction(CombatantState.Attacking);
            _events.Publish(new AttackResolvedEvent(attacker, defender, 0, false, true, source));
            return true;
        }

        var context = _damage.Calculate(new DamageContext(attacker, defender, _stats.Calculate(attacker, battle), defenderStats));
        var appliedDamage = defender.ReceiveDamage(context.Damage);
        attacker.SpendAction(CombatantState.Attacking);
        _events.Publish(new AttackResolvedEvent(attacker, defender, appliedDamage, context.IsCritical, false, source));
        if (!defender.IsAlive) _events.Publish(new StatusEvent($"{defender.Name}, {defender.Clan}, has fallen."));
        return true;
    }

    public bool ApplyAbilityHit(BattleState battle, Combatant attacker, Combatant defender, string source, bool stun)
    {
        if (!attacker.IsAlive || !defender.IsAlive || attacker.Clan == defender.Clan) return false;
        var defenderStats = _stats.Calculate(defender, battle);
        var context = _damage.Calculate(new DamageContext(attacker, defender, _stats.Calculate(attacker, battle), defenderStats));
        var appliedDamage = defender.ReceiveDamage(context.Damage);
        if (stun && defender.IsAlive) defender.Stun(1);
        _events.Publish(new AttackResolvedEvent(attacker, defender, appliedDamage, context.IsCritical, false, source));
        if (!defender.IsAlive) _events.Publish(new StatusEvent($"{defender.Name}, {defender.Clan}, has fallen."));
        return true;
    }
}
