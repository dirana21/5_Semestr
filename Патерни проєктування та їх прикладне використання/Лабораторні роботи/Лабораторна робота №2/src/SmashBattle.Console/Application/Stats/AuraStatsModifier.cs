using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Stats;

public sealed class AuraStatsModifier : IStatsModifier
{
    public EffectiveStats Apply(Combatant actor, EffectiveStats current, BattleState battle)
    {
        var leader = battle.Clans.Single(clan => clan.Type == actor.Clan).Leader;
        var aura = leader.Aura;
        if (!leader.IsAlive || leader.Id == actor.Id || aura is null ||
            leader.Position.ChebyshevDistanceTo(actor.Position) > aura.Radius)
            return current;

        return current with
        {
            MaximumHealth = (int)Math.Ceiling(current.MaximumHealth * aura.MaximumHealthMultiplier),
            MinimumDamage = (int)Math.Ceiling(current.MinimumDamage * aura.DamageMultiplier),
            MaximumDamage = (int)Math.Ceiling(current.MaximumDamage * aura.DamageMultiplier),
            Defense = current.Defense + aura.DefenseBonus,
            Speed = current.Speed + aura.SpeedBonus,
            DodgeChance = current.DodgeChance + aura.DodgeBonus
        };
    }
}
