using SmashBattle.Domain.Clans;

namespace SmashBattle.Application.Setup;

public sealed record BattleSetup(ClanType PlayerClan, int Seed);
