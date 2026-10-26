using System.Security.Cryptography;
using SmashBattle.Application.Randomness;

namespace SmashBattle.Infrastructure.Randomness;

public sealed class RandomSeedGenerator : ISeedGenerator
{
    public int Create() => RandomNumberGenerator.GetInt32(int.MaxValue);
}
