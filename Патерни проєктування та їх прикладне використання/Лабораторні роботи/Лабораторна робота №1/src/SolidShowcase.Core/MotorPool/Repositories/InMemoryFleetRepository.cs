namespace SolidShowcase.Core;

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
