using SmashBattle.Domain.Clans;

namespace SmashBattle.Creation.Names;

public interface INameProvider
{
    string Next(ClanType clan);
}
