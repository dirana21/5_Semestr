namespace SolidShowcase.Core;

public interface IFleetRepository
{
    IReadOnlyList<Driver> Drivers { get; }
    IReadOnlyList<Vehicle> Vehicles { get; }
    IReadOnlyList<Trip> Trips { get; }
    void AddDriver(Driver driver);
    void AddVehicle(Vehicle vehicle);
    void AddTrip(Trip trip);
}
