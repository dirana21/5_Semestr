using SmashBattle.Application.Randomness;

namespace SmashBattle.Application.Combat;

public sealed class RollDamageStage : DamageStage
{
    private readonly IRandomSource _random;

    public RollDamageStage(IRandomSource random) => _random = random;

    protected override void Process(DamageContext context) =>
        context.Damage = _random.Next(context.AttackerStats.MinimumDamage,
            context.AttackerStats.MaximumDamage + 1) + context.Attacker.Weapon.DamageBonus;
}
