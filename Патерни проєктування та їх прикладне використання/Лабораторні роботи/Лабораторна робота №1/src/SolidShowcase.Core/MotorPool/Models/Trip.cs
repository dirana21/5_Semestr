namespace SolidShowcase.Core;

public sealed class Trip(Guid id, CargoRequest request, Driver driver, Vehicle vehicle)
{
    public Guid Id { get; } = id;
    public CargoRequest Request { get; } = request;
    public Driver Driver { get; } = driver;
    public Vehicle Vehicle { get; } = vehicle;
    public bool IsCompleted { get; set; }
    public decimal Payment { get; set; }
}
