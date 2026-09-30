namespace SolidShowcase.Core;

public sealed class Vehicle(Guid id, string model, decimal capacityTons, int difficulty)
{
    public Guid Id { get; } = id;
    public string Model { get; } = model;
    public decimal CapacityTons { get; } = capacityTons;
    public int Difficulty { get; } = difficulty;
    public bool IsAvailable { get; set; } = true;
    public bool NeedsRepair { get; set; }
}
