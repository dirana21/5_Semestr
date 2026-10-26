using SmashBattle.Application.Randomness;

namespace SmashBattle.Application.Combat;

public sealed class CriticalDamageStage : DamageStage
{
    private readonly IRandomSource _random;

    public CriticalDamageStage(IRandomSource random) => _random = random;

    protected override void Process(DamageContext context)
    {
        context.IsCritical = (decimal)_random.NextDouble() < context.AttackerStats.CriticalChance;
        if (context.IsCritical) context.Damage = (int)Math.Ceiling(context.Damage * 1.5m);
    }
}
