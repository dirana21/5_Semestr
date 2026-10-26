namespace SmashBattle.Domain.Combatants;

public sealed record CombatStats(
    int MaximumHealth,
    int MinimumDamage,
    int MaximumDamage,
    int Defense,
    decimal Speed,
    decimal CriticalChance,
    decimal DodgeChance,
    int Initiative);
