namespace SmashBattle.Application.Combat;

public abstract class DamageStage : IDamageStage
{
    private IDamageStage? _next;

    public IDamageStage SetNext(IDamageStage next)
    {
        _next = next;
        return next;
    }

    public void Handle(DamageContext context)
    {
        Process(context);
        _next?.Handle(context);
    }

    protected abstract void Process(DamageContext context);
}
