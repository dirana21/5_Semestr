using SmashBattle.Domain.Abilities;
using SmashBattle.Domain.Auras;
using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Equipment;

namespace SmashBattle.Domain.Combatants;

public sealed class Combatant : IBattleComponent
{
    public Combatant(
        Guid id,
        string name,
        ClanType clan,
        char symbol,
        CombatStats baseStats,
        WeaponDefinition weapon,
        AbilityDefinition ability,
        Position position,
        bool isLeader,
        AuraDefinition? aura)
    {
        Id = id;
        Name = name;
        Clan = clan;
        Symbol = symbol;
        BaseStats = baseStats;
        Weapon = weapon;
        Ability = ability;
        Position = position;
        IsLeader = isLeader;
        Aura = aura;
        CurrentHealth = baseStats.MaximumHealth;
    }

    public Guid Id { get; }
    public string Name { get; }
    public ClanType Clan { get; }
    public char Symbol { get; }
    public CombatStats BaseStats { get; }
    public WeaponDefinition Weapon { get; }
    public AbilityDefinition Ability { get; }
    public AuraDefinition? Aura { get; }
    public bool IsLeader { get; }
    public Position Position { get; private set; }
    public int CurrentHealth { get; private set; }
    public decimal MovementPoints { get; private set; }
    public int AbilityCooldown { get; private set; }
    public int StunRounds { get; private set; }
    public int TemporaryMaximumHealthBonus { get; private set; }
    public CombatantState State { get; private set; } = CombatantState.Idle;
    public bool HasUsedAction { get; private set; }
    public bool IsAlive => State != CombatantState.Dead;

    public void BeginTurn(decimal speed)
    {
        HasUsedAction = false;
        if (AbilityCooldown > 0) AbilityCooldown--;
        if (StunRounds > 0)
        {
            StunRounds--;
            State = CombatantState.Stunned;
            return;
        }

        MovementPoints += speed;
        State = CombatantState.Idle;
    }

    public void MoveTo(Position position, decimal cost)
    {
        Position = position;
        MovementPoints = Math.Max(0, MovementPoints - cost);
        State = CombatantState.Moving;
    }

    public void SpendAction(CombatantState state)
    {
        HasUsedAction = true;
        State = state;
    }

    public void StartAbilityCooldown() => AbilityCooldown = Ability.CooldownRounds;
    public void Stun(int rounds) => StunRounds = Math.Max(StunRounds, rounds);

    public int ReceiveDamage(int damage)
    {
        var applied = Math.Min(CurrentHealth, Math.Max(0, damage));
        CurrentHealth -= applied;
        if (CurrentHealth == 0) State = CombatantState.Dead;
        return applied;
    }

    public void ApplyMaximumHealthBonus(int bonus, bool fillNewCapacity)
    {
        bonus = Math.Max(0, bonus);
        if (fillNewCapacity && bonus > TemporaryMaximumHealthBonus)
            CurrentHealth += bonus - TemporaryMaximumHealthBonus;
        TemporaryMaximumHealthBonus = bonus;
        CurrentHealth = Math.Min(CurrentHealth, BaseStats.MaximumHealth + TemporaryMaximumHealthBonus);
    }

    public IEnumerable<Combatant> GetCombatants()
    {
        yield return this;
    }

    public void Restore(int currentHealth, Position position, decimal movementPoints, int cooldown, int stunRounds,
        bool hasUsedAction, CombatantState state, int temporaryMaximumHealthBonus)
    {
        CurrentHealth = Math.Clamp(currentHealth, 0, BaseStats.MaximumHealth * 2);
        Position = position;
        MovementPoints = Math.Max(0, movementPoints);
        AbilityCooldown = Math.Max(0, cooldown);
        StunRounds = Math.Max(0, stunRounds);
        HasUsedAction = hasUsedAction;
        TemporaryMaximumHealthBonus = Math.Max(0, temporaryMaximumHealthBonus);
        State = CurrentHealth == 0 ? CombatantState.Dead : state;
    }
}
