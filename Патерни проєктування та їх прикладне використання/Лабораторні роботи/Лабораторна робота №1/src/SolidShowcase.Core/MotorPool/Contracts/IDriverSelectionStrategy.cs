namespace SolidShowcase.Core;

public interface IDriverSelectionStrategy
{
    Driver Select(IReadOnlyCollection<Driver> drivers, CargoRequest request, Vehicle vehicle);
}
