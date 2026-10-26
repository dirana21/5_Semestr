using SmashBattle.Application.UseCases;

namespace SmashBattle.Presentation.Menus;

public sealed class MainMenu
{
    private readonly StartBattleUseCase _startBattle;
    private readonly ShowClanCompositionUseCase _showComposition;
    private readonly ShowClanLeadersUseCase _showLeaders;
    private readonly ShowPatternsUseCase _showPatterns;

    public MainMenu(StartBattleUseCase startBattle, ShowClanCompositionUseCase showComposition,
        ShowClanLeadersUseCase showLeaders, ShowPatternsUseCase showPatterns)
    {
        _startBattle = startBattle;
        _showComposition = showComposition;
        _showLeaders = showLeaders;
        _showPatterns = showPatterns;
    }

    public void Run()
    {
        while (true)
        {
            Console.Clear();
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("SMASH BATTLE");
            Console.ResetColor();
            Console.WriteLine("1 - Play");
            Console.WriteLine("2 - Show clan composition");
            Console.WriteLine("3 - Show clan leaders");
            Console.WriteLine("4 - Show used patterns");
            Console.WriteLine("0 - Exit");
            Console.Write("Choice: ");
            switch (Console.ReadLine()?.Trim())
            {
                case "1": _startBattle.Execute(); break;
                case "2": _showComposition.Execute(); break;
                case "3": _showLeaders.Execute(); break;
                case "4": _showPatterns.Execute(); break;
                case "0": return;
            }
        }
    }
}
