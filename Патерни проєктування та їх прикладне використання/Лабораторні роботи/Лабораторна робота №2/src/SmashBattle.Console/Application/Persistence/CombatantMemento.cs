using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Application.Persistence;

public sealed record CombatantMemento(
    string Name,
    ClanType Clan,
    int CurrentHealth,
    Position Position,
    decimal MovementPoints,
    int AbilityCooldown,
    int StunRounds,
    bool HasUsedAction,
    CombatantState State,
    int TemporaryMaximumHealthBonus);
