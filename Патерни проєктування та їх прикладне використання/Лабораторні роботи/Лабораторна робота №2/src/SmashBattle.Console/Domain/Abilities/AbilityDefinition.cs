namespace SmashBattle.Domain.Abilities;

public sealed record AbilityDefinition(string Name, int Range, int AreaRadius, int CooldownRounds);
