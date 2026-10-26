namespace SmashBattle.Domain.Combatants;

public sealed record EffectiveStats(
    int MaximumHealth,
    int MinimumDamage,
    int MaximumDamage,
    int Defense,
    decimal Speed,
    decimal CriticalChance,
    decimal DodgeChance);
