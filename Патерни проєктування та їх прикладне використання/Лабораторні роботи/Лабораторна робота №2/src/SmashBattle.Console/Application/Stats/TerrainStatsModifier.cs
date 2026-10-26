using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;
using SmashBattle.Domain.World;

namespace SmashBattle.Application.Stats;

public sealed class TerrainStatsModifier : IStatsModifier
{
    public EffectiveStats Apply(Combatant actor, EffectiveStats current, BattleState battle)
    {
        var terrain = battle.Map.TerrainAt(actor.Position);
        return (actor.Clan, terrain) switch
        {
            (ClanType.Elfis, TerrainType.Forest) => current with { DodgeChance = current.DodgeChance + 0.10m },
            (ClanType.Dwargon, TerrainType.Rocks) => current with { Defense = current.Defense + 3 },
            (ClanType.Wrumper, TerrainType.Plain) => current with
            {
                MinimumDamage = (int)Math.Ceiling(current.MinimumDamage * 1.10m),
                MaximumDamage = (int)Math.Ceiling(current.MaximumDamage * 1.10m)
            },
            (_, TerrainType.Hill) when actor.Weapon.Range > 1 => current with
            {
                MinimumDamage = (int)Math.Ceiling(current.MinimumDamage * 1.15m),
                MaximumDamage = (int)Math.Ceiling(current.MaximumDamage * 1.15m)
            },
            _ => current
        };
    }
}
