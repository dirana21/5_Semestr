namespace SolidShowcase.Core;

public sealed record CargoRequest(
    Guid Id,
    string Destination,
    string CargoType,
    decimal WeightTons,
    int DistanceKm,
    int RequiredExperience);
