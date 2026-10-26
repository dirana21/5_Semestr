using SmashBattle.Application.Battle;

namespace SmashBattle.Application.AI;

public interface IAiController
{
    void TakeTurn(BattleSession session);
}
