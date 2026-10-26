using SmashBattle.Application.Battle;

namespace SmashBattle.Bootstrap;

public sealed record BattleRuntime(BattleSession Session, BattleLoop Loop);
