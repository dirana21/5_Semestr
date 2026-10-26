namespace SmashBattle.Application.Combat;

public sealed class DamagePipeline
{
    private readonly IDamageStage _first;

    public DamagePipeline(RollDamageStage roll, CriticalDamageStage critical, DefenseDamageStage defense, MinimumDamageStage minimum)
    {
        _first = roll;
        roll.SetNext(critical).SetNext(defense).SetNext(minimum);
    }

    public DamageContext Calculate(DamageContext context)
    {
        _first.Handle(context);
        return context;
    }
}
