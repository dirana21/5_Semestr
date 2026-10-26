using SmashBattle.Domain.Clans;

namespace SmashBattle.Application.Persistence;

public sealed record BattleMemento(
    int Seed,
    ClanType PlayerClan,
    ulong RandomState,
    int Round,
    int TurnIndex,
    IReadOnlyList<CombatantMemento> Combatants);
