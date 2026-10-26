namespace SmashBattle.Application.Combat;

public sealed class MinimumDamageStage : DamageStage
{
    protected override void Process(DamageContext context) => context.Damage = Math.Max(1, context.Damage);
}
