namespace SolidShowcase.Core;

public sealed class Driver(Guid id, string name, int experienceYears)
{
    public Guid Id { get; } = id;
    public string Name { get; } = name;
    public int ExperienceYears { get; } = experienceYears;
    public bool IsAvailable { get; set; } = true;
}

public sealed class Vehicle(Guid id, string model, decimal capacityTons, int difficulty)
{
    public Guid Id { get; } = id;
    public string Model { get; } = model;
    public decimal CapacityTons { get; } = capacityTons;
    public int Difficulty { get; } = difficulty;
    public bool IsAvailable { get; set; } = true;
    public bool NeedsRepair { get; set; }
}

public sealed record CargoRequest(Guid Id, string Destination, string CargoType, decimal WeightTons, int DistanceKm, int RequiredExperience);

public sealed class Trip(Guid id, CargoRequest request, Driver driver, Vehicle vehicle)
{
    public Guid Id { get; } = id;
    public CargoRequest Request { get; } = request;
    public Driver Driver { get; } = driver;
    public Vehicle Vehicle { get; } = vehicle;
    public bool IsCompleted { get; set; }
    public decimal Payment { get; set; }
}

public interface IDriverSelectionStrategy
{
    Driver Select(IReadOnlyCollection<Driver> drivers, CargoRequest request, Vehicle vehicle);
}

public interface IVehicleSelectionStrategy
{
    Vehicle Select(IReadOnlyCollection<Vehicle> vehicles, CargoRequest request);
}

public interface IFleetRepository
{
    IReadOnlyList<Driver> Drivers { get; }
    IReadOnlyList<Vehicle> Vehicles { get; }
    IReadOnlyList<Trip> Trips { get; }
    void AddDriver(Driver driver);
    void AddVehicle(Vehicle vehicle);
    void AddTrip(Trip trip);
}

public sealed class InMemoryFleetRepository : IFleetRepository
{
    private readonly List<Driver> _drivers;
    private readonly List<Vehicle> _vehicles;
    private readonly List<Trip> _trips = [];

    public InMemoryFleetRepository()
    {
        _drivers =
        [
            new Driver(Guid.NewGuid(), "Олексій Бондар", 8),
            new Driver(Guid.NewGuid(), "Марія Коваль", 5),
            new Driver(Guid.NewGuid(), "Іван Мельник", 2)
        ];
        _vehicles =
        [
            new Vehicle(Guid.NewGuid(), "Mercedes Sprinter", 3.5m, 2),
            new Vehicle(Guid.NewGuid(), "MAN TGL", 8m, 4),
            new Vehicle(Guid.NewGuid(), "Volvo FH", 22m, 7)
        ];
    }

    public IReadOnlyList<Driver> Drivers => _drivers;
    public IReadOnlyList<Vehicle> Vehicles => _vehicles;
    public IReadOnlyList<Trip> Trips => _trips;
    public void AddDriver(Driver driver) => _drivers.Add(driver);
    public void AddVehicle(Vehicle vehicle) => _vehicles.Add(vehicle);
    public void AddTrip(Trip trip) => _trips.Add(trip);
}

public sealed class ExperienceDriverSelectionStrategy(SolidTracer tracer) : IDriverSelectionStrategy
{
    public Driver Select(IReadOnlyCollection<Driver> drivers, CargoRequest request, Vehicle vehicle)
    {
        tracer.Add(
            "Автобаза",
            "Підбір водія",
            "ExperienceDriverSelectionStrategy.Select()",
            SolidPrinciple.O,
            "Open Closed Principle",
            "Правило призначення водія винесене у стратегію. Інший алгоритм можна додати без зміни DispatchService.",
            "return drivers\n    .Where(x => x.IsAvailable)\n    .Where(x => x.ExperienceYears >= required)\n    .OrderBy(x => x.ExperienceYears)\n    .First();",
            2);

        var required = Math.Max(request.RequiredExperience, vehicle.Difficulty / 2);
        return drivers
            .Where(driver => driver.IsAvailable && driver.ExperienceYears >= required)
            .OrderBy(driver => driver.ExperienceYears)
            .FirstOrDefault()
            ?? throw new InvalidOperationException("Немає доступного водія з необхідним стажем.");
    }
}

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
