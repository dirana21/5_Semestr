# Шпаргалка для объяснения проекта

Этот файл специально написан как последовательность «откуда пришло значение → куда мы его передали → кто его обработал». Код и интерфейс игры английские, а пояснения здесь русские.

## 1. Запуск программы

1. `Program.cs` настраивает UTF-8 и вызывает `GameCompositionRoot.Create().Run()`.
2. В `GameCompositionRoot.Create()` создаётся общее состояние меню `GameState` и четыре отдельных use case.
3. Получив пункт `1`, `MainMenu` передаёт управление в `StartBattleUseCase.Execute()`.
4. `BattleSetupReader` получает от пользователя клан и необязательный seed. Если строка пустая, он запрашивает значение у `RandomSeedGenerator`. Здесь мы только читаем данные — бой ещё не создаётся.
5. `StartBattleUseCase` передаёт эти два значения в `BattleRuntimeFactory.Create(playerClan, seed)`.
6. `BattleRuntimeFactory` связывает зависимости, но не считает урон и не двигает персонажей.

Фраза на защите: «`Program` ничего не знает об игре. Он передаёт запуск в composition root, а тот только соединяет небольшие классы».

## 2. Как seed превращается в одинаковый бой

1. `BattleRuntimeFactory` передаёт seed в `SeededRandomSource`.
2. Тот же объект случайности получает `MapGenerator`, `GeneratedNameProvider`, `ClanFactory` и боевой конвейер.
3. `BattleBuilder.Build()` сначала просит `MapGenerator` создать карту, потом получает три фабрики из `ClanFactoryProvider`.
4. `ElfisClanFactory`, `DwargonClanFactory` и `WrumperClanFactory` переопределяют фабричный метод `CreatePrototype()`; общий `ClanFactoryBase` затем вызывает `CombatantPrototype.Clone()`.
5. Поэтому один seed повторяет местность, составы, имена, оружие и случайные броски в том же порядке.

Здесь показываем паттерны Builder, Abstract Factory и Prototype.

## 3. Как создаётся глава и аура

1. `ClanFactoryBase.Create()` выбирает случайный `leaderIndex`.
2. Для этого индекса в `CombatantPrototype.Clone()` передаётся `isLeader = true`.
3. Прототип увеличивает максимальное здоровье на 50%, урон на 20%, инициативу на 2 и передаёт персонажу описание ауры.
4. После создания клана `BattleBuilder` передаёт его в `ClanLeadershipRegistry.Register()`.
5. Во время расчёта характеристик `EffectiveStatsCalculator` передаёт базовые значения последовательно в `AuraStatsModifier` и `TerrainStatsModifier`.
6. `AuraStatsModifier` проверяет: глава жив, цель союзная, это не сам глава, расстояние не больше 3. Только после этого добавляет бонус.
7. Для каменной ауры `AuraService.Initialize()` реально добавляет временный запас HP, а `Refresh()` снимает его после выхода из радиуса или смерти главы; это не просто число в HUD.

Фраза на защите: «Персонаж не содержит `if` по каждой ауре. Бонус — отдельный декоратор характеристик, поэтому новую ауру можно добавить без изменения боя».

## 4. Как строится жёлтая область движения

1. В начале хода `TurnScheduler` передаёт эффективную скорость в `Combatant.BeginTurn()`.
2. Скорость прибавляется к накопленным `MovementPoints`. Поэтому гном со скоростью 2 не теряет остаток: после двух ходов у него 4 очка.
3. `BattleSession.RefreshReachableArea()` передаёт карту и текущего персонажа в `ReachableAreaFinder.Find()`.
4. `ReachableAreaFinder` запускает алгоритм Дейкстры. Для каждой соседней клетки он спрашивает цену у `MovementCostCalculator`.
5. `MovementCostCalculator` передаёт тип клетки в `TerrainCatalog`, а затем применяет расовую скидку: воин на равнине, эльф в лесу, гном на камнях платят 2 очка.
6. Вода возвращает `IsPassable = false`, а занятые клетки заранее исключаются.
7. Готовый словарь достижимых координат возвращается в `BattleSession`.
8. `ConsoleBattleRenderer` только читает этот словарь и красит соответствующие клетки тёмно-жёлтым.

Важно: renderer не решает, можно ли пройти. Он показывает уже рассчитанный результат.

## 5. Что происходит после клика по клетке

1. `WindowsConsoleInputReader` читает клавиши через стандартный `Console.ReadKey`, а координаты мыши получает из Win32. Оба варианта он превращает в единый `GameInput`. Это Adapter.
2. `PlayerTurnController` видит тип события и передаёт мышь в `PlayerMouseController`.
3. `PlayerMouseController` передаёт координаты в `ConsoleBattleRenderer.ScreenToWorld()` и получает координаты мира 50×50.
4. Если режим `Move`, mouse-controller создаёт `MoveCommand` и передаёт его в `CommandDispatcher`.
5. `MoveCommand.Execute()` передаёт персонажа, цель и ранее рассчитанную область в `MovementService.Move()`.
6. `MovementService` проверяет цену, вызывает `Combatant.MoveTo()` и публикует `MovementCompletedEvent`.
7. `BattleEventPublisher` передаёт событие подписчику `BattleLog`.
8. `MovementService` получает весь путь из `ReachableArea.PathTo()` и передаёт каждый отдельный шаг в `ConsoleMovementStepObserver`.
9. Observer обновляет координату на экране, показывает номер шага и делает паузу 240 мс. Поэтому персонаж видимо проходит маршрут, а не телепортируется.
10. После последней клетки справа появляется итоговая запись вида: `Aelrion moved from (2,2) to (4,2); cost 5.0.`

Так один клик проходит через Adapter → Controller → Command → Service → Domain → Observer.

## 6. Обычная атака и полный лог

1. Игрок нажимает `[ ATTACK ]`, затем кликает красного противника. Controller создаёт `AttackCommand`.
2. `AttackCommand` передаёт текущего бойца и выбранную цель в `CombatService.Attack()`.
3. `CombatService` сначала спрашивает `EffectiveStatsCalculator` об актуальных аурах и местности обоих персонажей.
4. Затем проверяется уклонение цели.
5. Если цель не уклонилась, создаётся `DamageContext` и передаётся в `DamagePipeline`.
6. `RollDamageStage` бросает базовый урон и добавляет оружие.
7. `CriticalDamageStage` проверяет шанс и при успехе умножает результат на 1.5.
8. `DefenseDamageStage` вычитает защиту; состояние `Defending` добавляет ещё 5.
9. `MinimumDamageStage` гарантирует минимум 1 единицу.
10. Результат передаётся в `Combatant.ReceiveDamage()`.
11. `AttackResolvedEvent` сохраняет имя атакующего, имя цели, источник, точный урон, крит, уклонение и оставшееся HP.
12. `ConsoleBattleLogRenderer` берёт последние 8 сообщений через `BattleLog.Latest(8)` и рисует их под картой на всю ширину. Клавиша `L` показывает весь список без удаления старых записей.

Пример объяснения: «Здесь `CombatService` передаёт единый `DamageContext` первому звену цепочки. Каждое звено меняет только свою часть расчёта и передаёт контекст дальше».

## 7. Уникальная способность

1. Кнопка `[ ABILITY ]` переводит `BattleSession.Mode` в `Ability`.
2. Клик по фиолетовой клетке создаёт `AbilityCommand` с центром области.
3. `AbilityService` проверяет дальность, cooldown и наличие врагов.
4. Для каждого врага внутри радиуса вызывается `CombatService.ApplyAbilityHit()`.
5. Для `Ground Slam` дополнительно вызывается `Combatant.Stun(1)`.
6. После обработки всех целей способность тратит действие и запускает перезарядку.

`Whirlwind`: центр рядом с воином, радиус 1, cooldown 3 раунда.  
`Arrow Rain`: дальность 6, радиус области 2, cooldown 4 раунда.  
`Ground Slam`: соседняя область, оглушение, cooldown 4 раунда.

## 8. Инициатива и завершение хода

1. `TurnScheduler.Start()` сортирует персонажей по инициативе, затем по скорости, HP и имени.
2. В интерфейсе активен только `Turns.Current`.
3. Движение не тратит основное действие. Атака, способность или защита выставляет `HasUsedAction = true`.
4. После действия ход не переключается автоматически: игрок нажимает `[ END TURN ]` или `E`.
5. `EndTurnCommand` передаёт управление в `TurnScheduler.EndTurn()`.
6. Scheduler пропускает мёртвых, увеличивает номер раунда после полного круга и вызывает `BeginTurn()` следующего персонажа.
7. `Tab` не нарушает инициативу: он выбирает следующую вражескую цель для `Space`/`Q`, но не меняет того, чей сейчас ход.

## 9. Как ходит AI

1. `BattleLoop` видит, что текущий персонаж принадлежит не игровому клану.
2. По типу клана `AiControllerProvider` возвращает нужную стратегию.
3. Все три стратегии наследуют `AiTurnTemplate`, где задан общий шаблон: выбрать цель → попробовать способность → попробовать атаку → выбрать клетку → пройти → снова атаковать → защищаться.
4. `AggressiveAiController` выбирает ближайшего врага.
5. `RangedAiController` предпочитает раненую цель и оценивает клетку так, чтобы сохранить дистанцию.
6. `DefensiveAiController` ищет угрозу, ближайшую к своему главе.

Здесь Strategy меняет решение, а Template Method сохраняет общий порядок хода.

## 10. Сохранение F5 и загрузка F9

1. По F5 `PlayerTurnController` вызывает `BattleMementoFactory.Capture()`.
2. Фабрика переносит нужное состояние каждого бойца в `CombatantMemento`, не сериализуя сервисы и renderer.
3. `BattleSaveStore` получает общий `BattleMemento` и записывает JSON в `%LocalAppData%\SmashBattle\battle-save.json`.
4. По F9 store читает JSON и передаёт снимок обратно в `BattleMementoFactory.Restore()`.
5. Restore находит бойца по клану и имени, передаёт значения в `Combatant.Restore()` и возвращает индекс текущего хода в `TurnScheduler`.

## 11. Где менять правила

- Базовые числа рас: `CombatantPrototypeCatalog.cs`.
- Оружие и дальность: `WeaponCatalog.cs`.
- Размер и вероятности местности: `MapGenerator.cs`.
- Цена клетки: `TerrainCatalog.cs` и `MovementCostCalculator.cs`.
- Формула урона: отдельные файлы в `Application/Combat/*DamageStage.cs`.
- Ауры и ландшафтные бонусы: файлы в `Application/Stats`.
- AI: один класс на клан в `Application/AI`.
- Цвета и расположение HUD: `ConsoleBattleRenderer.cs` и `ConsoleLayout.cs`.
- Разделение мыши и клавиатуры: `PlayerTurnController.cs`.
- Смысл клика: `PlayerMouseController.cs`.
- Клавиши: `PlayerKeyboardController.cs`.

## 12. Что особенно показать преподавателю

1. Запустить с указанным seed или оставить строку пустой для случайного значения, затем сделать ход по клетке с жёлтым контуром `□`.
2. Нажать Attack, выбрать красную цель и показать точную строку полного лога.
3. Показать четыре маленьких класса цепочки урона вместо одной огромной формулы.
4. Открыть `IPlayerCommand`, затем `MoveCommand`, `AttackCommand`, `AbilityCommand`, `EndTurnCommand`.
5. Показать, что Win32-код находится только в `Infrastructure/ConsoleInput` и не попал в боевую логику.
6. Нажать F5, сделать действие, нажать F9 и продемонстрировать возврат состояния.
7. Запустить тесты и показать, что правила проверяются отдельно от консоли.
