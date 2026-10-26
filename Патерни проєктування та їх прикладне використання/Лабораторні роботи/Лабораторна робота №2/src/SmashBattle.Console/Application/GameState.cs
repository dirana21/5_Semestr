using SmashBattle.Domain.Battle;

namespace SmashBattle.Application;

public sealed class GameState
{
    public BattleState? LastBattle { get; set; }
}
