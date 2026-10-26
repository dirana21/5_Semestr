using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Events;

public sealed record AttackResolvedEvent(
    Combatant Attacker,
    Combatant Defender,
    int Damage,
    bool IsCritical,
    bool WasDodged,
    string Source) : IBattleEvent
{
    public string Message => WasDodged
        ? $"{Defender.Name} dodged {Attacker.Name}'s {Source}."
        : $"{Attacker.Name} > {Defender.Name}: {Damage} DMG | {Source}{(IsCritical ? " | CRITICAL" : string.Empty)} | " +
          $"{Defender.CurrentHealth} HP left.";
}
