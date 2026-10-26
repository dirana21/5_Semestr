using SmashBattle.Domain.Clans;
using SmashBattle.Domain.Combatants;

namespace SmashBattle.Creation.Clans;

public sealed class ClanLeadershipRegistry
{
    private static readonly Lazy<ClanLeadershipRegistry> LazyInstance = new(() => new ClanLeadershipRegistry());
    private readonly Dictionary<ClanType, Combatant> _leaders = [];

    private ClanLeadershipRegistry() { }

    public static ClanLeadershipRegistry Instance => LazyInstance.Value;
    public IReadOnlyDictionary<ClanType, Combatant> Leaders => _leaders;

    public void Register(Clan clan) => _leaders[clan.Type] = clan.Leader;
    public void Clear() => _leaders.Clear();
}
