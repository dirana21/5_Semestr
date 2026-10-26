namespace SmashBattle.Domain.Auras;

public sealed record AuraDefinition(
    string Name,
    int Radius,
    decimal DamageMultiplier,
    int DefenseBonus,
    decimal SpeedBonus,
    decimal DodgeBonus,
    decimal MaximumHealthMultiplier);
