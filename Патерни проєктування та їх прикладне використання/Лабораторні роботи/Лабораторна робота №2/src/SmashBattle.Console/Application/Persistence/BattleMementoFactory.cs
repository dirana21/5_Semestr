using SmashBattle.Application.Battle;
using SmashBattle.Application.Randomness;

namespace SmashBattle.Application.Persistence;

public sealed class BattleMementoFactory
{
    private readonly IRandomSource _random;

    public BattleMementoFactory(IRandomSource random) => _random = random;

    public BattleMemento Capture(BattleSession session) => new(
        session.Battle.Seed,
        session.Battle.PlayerClan,
        _random.State,
        session.Battle.Round,
        session.Turns.CurrentIndex,
        session.Battle.Clans.SelectMany(clan => clan.Members).Select(actor => new CombatantMemento(
            actor.Name, actor.Clan, actor.CurrentHealth, actor.Position, actor.MovementPoints,
            actor.AbilityCooldown, actor.StunRounds, actor.HasUsedAction, actor.State,
            actor.TemporaryMaximumHealthBonus)).ToList());

    public void Restore(BattleSession session, BattleMemento memento)
    {
        _random.Restore(memento.RandomState);
        foreach (var saved in memento.Combatants)
        {
            var actor = session.Battle.Clans.Single(clan => clan.Type == saved.Clan).Members
                .Single(member => member.Name == saved.Name);
            actor.Restore(saved.CurrentHealth, saved.Position, saved.MovementPoints, saved.AbilityCooldown,
                saved.StunRounds, saved.HasUsedAction, saved.State, saved.TemporaryMaximumHealthBonus);
        }

        session.Battle.Round = memento.Round;
        session.Turns.Restore(session.Battle, memento.TurnIndex);
        session.RefreshReachableArea();
    }
}
