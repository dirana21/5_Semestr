namespace SolidShowcase.Core;

public sealed class BestFitVehicleSelectionStrategy(SolidTracer tracer) : IVehicleSelectionStrategy
{
    public Vehicle Select(IReadOnlyCollection<Vehicle> vehicles, CargoRequest request)
    {
        tracer.Add(
            "Автобаза",
            "Підбір автомобіля",
            "BestFitVehicleSelectionStrategy.Select()",
            SolidPrinciple.S,
            "Single Responsibility Principle",
            "Стратегія відповідає лише за оптимальний вибір автомобіля за вантажопідйомністю.",
            "return vehicles\n    .Where(x => x.IsAvailable && !x.NeedsRepair)\n    .Where(x => x.CapacityTons >= request.WeightTons)\n    .OrderBy(x => x.CapacityTons)\n    .First();",
            2);

        return vehicles
            .Where(vehicle => vehicle.IsAvailable && !vehicle.NeedsRepair && vehicle.CapacityTons >= request.WeightTons)
            .OrderBy(vehicle => vehicle.CapacityTons)
            .FirstOrDefault()
            ?? throw new InvalidOperationException("Немає доступного автомобіля потрібної вантажопідйомності.");
    }
}
