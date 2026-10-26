using SmashBattle.Domain.Battle;

namespace SmashBattle.Application.Auras;

public sealed class AuraService
{
    public void Initialize(BattleState battle) => Refresh(battle, true);
    public void Refresh(BattleState battle) => Refresh(battle, false);

    private static void Refresh(BattleState battle, bool fillNewCapacity)
    {
        foreach (var clan in battle.Clans)
        {
            var leader = clan.Leader;
            foreach (var member in clan.Members)
            {
                var receivesAura = leader.IsAlive && member.IsAlive && member.Id != leader.Id && leader.Aura is not null &&
                                   leader.Position.ChebyshevDistanceTo(member.Position) <= leader.Aura.Radius;
                var multiplier = receivesAura ? leader.Aura!.MaximumHealthMultiplier : 1m;
                var bonus = (int)Math.Ceiling(member.BaseStats.MaximumHealth * (multiplier - 1m));
                member.ApplyMaximumHealthBonus(bonus, fillNewCapacity);
            }
        }
    }
}
