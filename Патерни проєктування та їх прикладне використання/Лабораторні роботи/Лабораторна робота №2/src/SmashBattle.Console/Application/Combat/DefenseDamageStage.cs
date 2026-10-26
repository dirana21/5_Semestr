using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Combat;

public sealed class DefenseDamageStage : DamageStage
{
    protected override void Process(DamageContext context)
    {
        var defense = context.DefenderStats.Defense;
        if (context.Defender.State == CombatantState.Defending) defense += 5;
        context.Damage -= defense;
    }
}
