using SmashBattle.Domain.Battle;
using SmashBattle.Domain.Clans;

namespace SmashBattle.Application.Battle;

public sealed class VictoryCondition
{
    public ClanType? GetWinner(BattleState battle)
    {
        var livingClans = battle.Clans.Where(clan => clan.IsAlive).ToList();
        return livingClans.Count == 1 ? livingClans[0].Type : null;
    }
}
