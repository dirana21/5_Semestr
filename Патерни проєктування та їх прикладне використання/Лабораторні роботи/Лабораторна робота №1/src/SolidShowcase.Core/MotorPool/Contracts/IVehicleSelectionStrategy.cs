namespace SolidShowcase.Core;

public interface IVehicleSelectionStrategy
{
    Vehicle Select(IReadOnlyCollection<Vehicle> vehicles, CargoRequest request);
}
