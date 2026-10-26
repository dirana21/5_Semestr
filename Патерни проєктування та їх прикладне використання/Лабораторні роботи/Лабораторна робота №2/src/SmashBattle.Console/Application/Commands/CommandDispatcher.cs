namespace SmashBattle.Application.Commands;

public sealed class CommandDispatcher
{
    public bool Dispatch(IPlayerCommand command) => command.Execute();
}
