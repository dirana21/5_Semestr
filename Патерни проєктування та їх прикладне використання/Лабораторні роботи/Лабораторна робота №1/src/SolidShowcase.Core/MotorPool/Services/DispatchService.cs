namespace SolidShowcase.Core;

public sealed class DispatchService(
    IFleetRepository repository,
    IDriverSelectionStrategy driverSelection,
    IVehicleSelectionStrategy vehicleSelection,
    SolidTracer tracer)
{
    public Trip Dispatch(CargoRequest request)
    {
        tracer.Add(
            "Автобаза",
            "Створення рейсу",
            "DispatchService.Dispatch()",
            SolidPrinciple.D,
            "Dependency Inversion Principle",
            "Диспетчер залежить від IFleetRepository та стратегій вибору, а не від конкретних списків і алгоритмів.",
            "public Trip Dispatch(CargoRequest request)\n{\n    var vehicle = _vehicleSelection.Select(...);\n    var driver = _driverSelection.Select(...);\n    return CreateTrip(request, driver, vehicle);\n}",
            3);

        var vehicle = vehicleSelection.Select(repository.Vehicles, request);
        var driver = driverSelection.Select(repository.Drivers, request, vehicle);
        driver.IsAvailable = false;
        vehicle.IsAvailable = false;
        var trip = new Trip(Guid.NewGuid(), request, driver, vehicle);
        repository.AddTrip(trip);
        return trip;
    }

    public decimal Complete(Trip trip)
    {
        tracer.Add(
            "Автобаза",
            "Завершення рейсу",
            "DispatchService.Complete()",
            SolidPrinciple.I,
            "Interface Segregation Principle",
            "Сервіс використовує компактні контракти підбору. Алгоритми не змушені реалізовувати керування ремонтом або виплатами.",
            "trip.IsCompleted = true;\ntrip.Driver.IsAvailable = true;\ntrip.Vehicle.IsAvailable = !trip.Vehicle.NeedsRepair;\ntrip.Payment = distance * 6.5m;",
            2);

        trip.IsCompleted = true;
        trip.Driver.IsAvailable = true;
        trip.Vehicle.IsAvailable = !trip.Vehicle.NeedsRepair;
        trip.Payment = trip.Request.DistanceKm * 6.5m;
        return trip.Payment;
    }

    public void BreakVehicle(Trip trip)
    {
        tracer.Add(
            "Автобаза",
            "Поломка в рейсі",
            "DispatchService.BreakVehicle()",
            SolidPrinciple.S,
            "Single Responsibility Principle",
            "Стан автомобіля змінюється окремою операцією; підбір рейсу та ремонт не змішані в одному методі.",
            "trip.Vehicle.NeedsRepair = true;\ntrip.Vehicle.IsAvailable = false;",
            1);
        trip.Vehicle.NeedsRepair = true;
        trip.Vehicle.IsAvailable = false;
    }

    public void Repair(Vehicle vehicle)
    {
        tracer.Add(
            "Автобаза",
            "Завершення ремонту",
            "DispatchService.Repair()",
            SolidPrinciple.L,
            "Liskov Substitution Principle",
            "Після відновлення автомобіль знову відповідає контракту доступного транспортного засобу і може брати участь у підборі.",
            "vehicle.NeedsRepair = false;\nvehicle.IsAvailable = true;",
            2);
        vehicle.NeedsRepair = false;
        vehicle.IsAvailable = true;
    }
}
