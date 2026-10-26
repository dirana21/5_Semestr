using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Common;

namespace SmashBattle.Creation.Clans;

public interface IClanFactory
{
    ClanType ClanType { get; }
    Clan Create(IReadOnlyList<Position> spawnPositions);
}
