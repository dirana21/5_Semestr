using SmashBattle.Domain.Clans;

namespace SmashBattle.Creation.Clans;

public sealed class ClanFactoryProvider
{
    private readonly IReadOnlyDictionary<ClanType, IClanFactory> _factories;

    public ClanFactoryProvider(IEnumerable<IClanFactory> factories) =>
        _factories = factories.ToDictionary(factory => factory.ClanType);

    public IClanFactory Get(ClanType clan) => _factories[clan];
}
