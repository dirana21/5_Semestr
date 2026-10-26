namespace SmashBattle.Application.Combat;

public interface IDamageStage
{
    IDamageStage SetNext(IDamageStage next);
    void Handle(DamageContext context);
}
