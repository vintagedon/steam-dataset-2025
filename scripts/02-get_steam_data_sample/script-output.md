# Steam Data Collection: Run Summary & Log

## Run Summary

| Metric                 | Value                                     |
| :--------------------- | :---------------------------------------- |
| Generating Script | `get_steam_data_sample.py` (v1.1)         |
| Repository | `https://github.com/vintagedon/steam-dataset-2025` |
| Start Timestamp | `2025-08-31 14:00:12`                     |
| End Timestamp | `2025-08-31 14:05:24`                     |
| Duration | 5 minutes, 12 seconds                     |
| Parameters |                                           |
| _Target Game Count_    | `100`                                     |
| _Output File_          | `steam_data_sample.json`                  |
| Results |                                           |
| _Final Status_         | Success                                   |
| _Games Found_          | `100`                                     |
| _Total Apps Processed_ | `193`                                     |

---

## Script Output Log

```log
[2025-08-31 14:00:12] [INFO] - 🚀 Starting data collection run. Target: 100 games. Output: steam_data_sample.json
[2025-08-31 14:00:12] [INFO] - Fetching full Steam application list...
[2025-08-31 14:00:13] [INFO] - Successfully retrieved 263,899 total applications.
[2025-08-31 14:00:13] [INFO] - Filtered to 263,657 candidate apps (AppID > 2000).
[2025-08-31 14:00:13] [INFO] - (0/100) Processing AppID 2267870: Stewart The Fox
[2025-08-31 14:00:13] [INFO] -    ✅ Found Game: Stewart The Fox | Price: Free
[2025-08-31 14:00:14] [INFO] - (1/100) Processing AppID 3210840: Ninja Numpties
[2025-08-31 14:00:14] [INFO] -    ✅ Found Game: Ninja Numpties | Price: $2.99
[2025-08-31 14:00:16] [INFO] - (2/100) Processing AppID 2713920: Where's the Boat
[2025-08-31 14:00:16] [INFO] -    ✅ Found Game: Where's the Boat | Price: $11.99
[2025-08-31 14:00:17] [INFO] - (3/100) Processing AppID 1691310: Tactical Troops: Anthracite Shift Playtest
[2025-08-31 14:00:18] [INFO] -    ✅ Found Game: Tactical Troops: Anthracite Shift Playtest | Price: Free
[2025-08-31 14:00:19] [INFO] - (4/100) Processing AppID 1666190: Yellow Ballman
[2025-08-31 14:00:19] [INFO] -    ✅ Found Game: Yellow Ballman | Price: $3.99
[2025-08-31 14:00:21] [INFO] - (5/100) Processing AppID 222619: Train Simulator: Union Pacific DDA40X Centennial
[2025-08-31 14:00:21] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:22] [INFO] - (5/100) Processing AppID 262000: Gabriel Knight - Sins of the Fathers
[2025-08-31 14:00:22] [INFO] -    ✅ Found Game: Gabriel Knight: Sins of the Fathers 20th Anniversary Edition | Price: $19.99
[2025-08-31 14:00:24] [INFO] - (6/100) Processing AppID 1297190: One Hundred Courage
[2025-08-31 14:00:24] [INFO] -    ✅ Found Game: One Hundred Courage | Price: $0.99
[2025-08-31 14:00:25] [INFO] - (7/100) Processing AppID 2682720: Caveman Skin
[2025-08-31 14:00:26] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:27] [INFO] - (7/100) Processing AppID 830640: DayZ Tools
[2025-08-31 14:00:27] [INFO] -    ✅ Found Game: DayZ Tools | Price: Free
[2025-08-31 14:00:29] [INFO] - (8/100) Processing AppID 2860620: AfroCobra
[2025-08-31 14:00:29] [INFO] -    ✅ Found Game: AfroCobra | Price: $0.99
[2025-08-31 14:00:30] [INFO] - (9/100) Processing AppID 1037690: BIOSZARD Corporation
[2025-08-31 14:00:30] [INFO] -    ✅ Found Game: BIOSZARD Corporation | Price: $0.89
[2025-08-31 14:00:32] [INFO] - (10/100) Processing AppID 1685351: Tiger Tank 59 Ⅰ Black Hill Fortress MP002
[2025-08-31 14:00:32] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:33] [INFO] - (10/100) Processing AppID 285330: RollerCoaster Tycoon 2: Triple Thrill Pack
[2025-08-31 14:00:34] [INFO] -    ✅ Found Game: RollerCoaster Tycoon® 2: Triple Thrill Pack | Price: $9.99
[2025-08-31 14:00:35] [INFO] - (11/100) Processing AppID 3287270: Roy Rattler Demo
[2025-08-31 14:00:35] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:37] [INFO] - (11/100) Processing AppID 2956780: An Archers Fate
[2025-08-31 14:00:37] [INFO] -    ✅ Found Game: An Archers Fate | Price: Free
[2025-08-31 14:00:38] [INFO] - (12/100) Processing AppID 2935490: The Land of the Magnates Soundtrack
[2025-08-31 14:00:38] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:40] [INFO] - (12/100) Processing AppID 1629690: RushOut
[2025-08-31 14:00:40] [INFO] -    ✅ Found Game: RushOut | Price: Free
[2025-08-31 14:00:41] [INFO] - (13/100) Processing AppID 3654770: Collectors Cove Demo
[2025-08-31 14:00:42] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:43] [INFO] - (13/100) Processing AppID 1665370: RPG Maker MV - Aethereal Planes Battlebacks Vol 2
[2025-08-31 14:00:43] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:45] [INFO] - (13/100) Processing AppID 1885790: Untravelled Planet
[2025-08-31 14:00:45] [INFO] -    ✅ Found Game: Untravelled Planet | Price: $5.99
[2025-08-31 14:00:46] [INFO] - (14/100) Processing AppID 1322670: Unity of Command II - DLC 1
[2025-08-31 14:00:46] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:48] [INFO] - (14/100) Processing AppID 319010: Hyperdimension Neptunia Re;Birth1 Histy's Beginner's Item
[2025-08-31 14:00:48] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:50] [INFO] - (14/100) Processing AppID 883670: V.T.
[2025-08-31 14:00:50] [INFO] -    ✅ Found Game: V.T. | Price: $12.99
[2025-08-31 14:00:51] [INFO] - (15/100) Processing AppID 1010210: The Crown of Leaves - OST
[2025-08-31 14:00:51] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:51] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:00:53] [INFO] - (15/100) Processing AppID 2353050: WTF: Waifu Tactical Force
[2025-08-31 14:00:53] [INFO] -    ✅ Found Game: WTF: Waifu Tactical Force | Price: Free
[2025-08-31 14:00:54] [INFO] - (16/100) Processing AppID 3605150: Pub Toilet Simulator 25
[2025-08-31 14:00:55] [INFO] -    ✅ Found Game: Pub Toilet Simulator 25 | Price: $4.99
[2025-08-31 14:00:56] [INFO] - (17/100) Processing AppID 2803480: Zombie Death Day Demo
[2025-08-31 14:00:56] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:00:58] [INFO] - (17/100) Processing AppID 315920: Stonerid
[2025-08-31 14:00:58] [INFO] -    ✅ Found Game: Stonerid | Price: $4.99
[2025-08-31 14:00:59] [INFO] - (18/100) Processing AppID 1907350: Arena Renovation - First Job
[2025-08-31 14:00:59] [INFO] -    ✅ Found Game: Arena Renovation - First Job | Price: Free
[2025-08-31 14:01:01] [INFO] - (19/100) Processing AppID 3472500: IN THE FACADE WE TRUST™ Soundtrack
[2025-08-31 14:01:01] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:03] [INFO] - (19/100) Processing AppID 3702570: Ravenhille: Awakened Demo
[2025-08-31 14:01:03] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:04] [INFO] - (19/100) Processing AppID 908474: Combat Fighter Pack
[2025-08-31 14:01:04] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:06] [INFO] - (19/100) Processing AppID 853884: Ultimate Sudoku Collection - Butterfly Pack
[2025-08-31 14:01:06] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:07] [INFO] - (19/100) Processing AppID 1281120: Desktop Agents - Cov1d-999 Soundtrack
[2025-08-31 14:01:07] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:09] [INFO] - (19/100) Processing AppID 2581460: Home Designer Blast - Ryan's Halloween Hallway
[2025-08-31 14:01:09] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:11] [INFO] - (19/100) Processing AppID 2426960: Summoners War
[2025-08-31 14:01:11] [INFO] -    ✅ Found Game: Summoners War | Price: Free
[2025-08-31 14:01:12] [INFO] - (20/100) Processing AppID 1860730: Foot Fetish Fortress VolTitan Vs. The Jundoh Empire Volume 1 Demo
[2025-08-31 14:01:12] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:14] [INFO] - (20/100) Processing AppID 478051: Zaccaria Pinball - Mystic Star Table
[2025-08-31 14:01:14] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:15] [INFO] - (20/100) Processing AppID 2629380: Transilio Demo
[2025-08-31 14:01:15] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:17] [INFO] - (20/100) Processing AppID 582910: Bleach: Bleach 102
[2025-08-31 14:01:17] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:19] [INFO] - (20/100) Processing AppID 1778020: The Resolve
[2025-08-31 14:01:19] [INFO] -    ✅ Found Game: The Resolve | Price: Free
[2025-08-31 14:01:21] [INFO] - (21/100) Processing AppID 1545700: Guns N' Runs
[2025-08-31 14:01:21] [INFO] -    ✅ Found Game: Guns N' Runs | Price: $6.99
[2025-08-31 14:01:22] [INFO] - (22/100) Processing AppID 2137310: Contraption Simulator Demo
[2025-08-31 14:01:22] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:24] [INFO] - (22/100) Processing AppID 1204710: Void Breach
[2025-08-31 14:01:24] [INFO] -    ✅ Found Game: Void Breach | Price: $1.99
[2025-08-31 14:01:25] [INFO] - (23/100) Processing AppID 3728350: RAFT Days Demo
[2025-08-31 14:01:26] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:27] [INFO] - (23/100) Processing AppID 2846690: Ribbit Rampage
[2025-08-31 14:01:27] [INFO] -    ✅ Found Game: Ribbit Rampage | Price: Free
[2025-08-31 14:01:29] [INFO] - (24/100) Processing AppID 1296770: Her New Memory
[2025-08-31 14:01:29] [INFO] -    ✅ Found Game: Her New Memory - Hentai Simulator | Price: $9.99
[2025-08-31 14:01:30] [INFO] - (25/100) Processing AppID 2849880: Three Kingdoms: The Blood Moon Demo
[2025-08-31 14:01:30] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:32] [INFO] - (25/100) Processing AppID 28061: Tactical Enhancement Pack
[2025-08-31 14:01:32] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:32] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:01:33] [INFO] - (25/100) Processing AppID 552110: Puzzle Pirates: Dark Seas
[2025-08-31 14:01:34] [INFO] -    ✅ Found Game: Puzzle Pirates: Dark Seas | Price: Free
[2025-08-31 14:01:35] [INFO] - (26/100) Processing AppID 2887480: Pool of Madness Demo
[2025-08-31 14:01:35] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:37] [INFO] - (26/100) Processing AppID 2139990: Starship Troopers: Terran Command - Raising Hell
[2025-08-31 14:01:37] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:38] [INFO] - (26/100) Processing AppID 2025310: Sigh of the Abyss
[2025-08-31 14:01:38] [INFO] -    ✅ Found Game: Sigh of the Abyss | Price: $17.99
[2025-08-31 14:01:40] [INFO] - (27/100) Processing AppID 1264113: Simplode Suite - Basic Window Management
[2025-08-31 14:01:40] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:42] [INFO] - (27/100) Processing AppID 442328: Forest Ground - Part 12: Nanomeshing Branches
[2025-08-31 14:01:42] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:43] [INFO] - (27/100) Processing AppID 1703620: 胖子灵异事件簿~廊之篇~
[2025-08-31 14:01:43] [INFO] -    ✅ Found Game: Chubmen's Strange Case File~Chapter Of Corridor~ | Price: $2.99
[2025-08-31 14:01:45] [INFO] - (28/100) Processing AppID 318073: Happy Wars - Fast Food Cleric Set
[2025-08-31 14:01:45] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:46] [INFO] - (28/100) Processing AppID 3803990: Our Summer Festival 2
[2025-08-31 14:01:46] [INFO] -    ✅ Found Game: Our Summer Festival 2 | Price: $16.99
[2025-08-31 14:01:48] [INFO] - (29/100) Processing AppID 864880: Beasts & Chests
[2025-08-31 14:01:48] [INFO] -    ✅ Found Game: Beasts&Chests | Price: $0.99
[2025-08-31 14:01:50] [INFO] - (30/100) Processing AppID 3566230: Become Barista!
[2025-08-31 14:01:50] [INFO] -    ✅ Found Game: Become Barista! | Price: Free
[2025-08-31 14:01:51] [INFO] - (31/100) Processing AppID 2590330: Dino Run 2
[2025-08-31 14:01:51] [INFO] -    ✅ Found Game: Dino Run 2 | Price: Free
[2025-08-31 14:01:53] [INFO] - (32/100) Processing AppID 1140420: Quantism
[2025-08-31 14:01:53] [INFO] -    ✅ Found Game: Quantism | Price: $1.99
[2025-08-31 14:01:54] [INFO] - (33/100) Processing AppID 2413050: Retrowave World
[2025-08-31 14:01:55] [INFO] -    ✅ Found Game: Retrowave World | Price: $9.99
[2025-08-31 14:01:56] [INFO] - (34/100) Processing AppID 2175010: Seasick Demo
[2025-08-31 14:01:56] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:01:58] [INFO] - (34/100) Processing AppID 2086520: 萤火虫动映
[2025-08-31 14:01:58] [INFO] -    ✅ Found Game: Firefly Studio | Price: Free
[2025-08-31 14:01:59] [INFO] - (35/100) Processing AppID 2720770: A Game´s Tale Demo
[2025-08-31 14:01:59] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:01] [INFO] - (35/100) Processing AppID 1761470: Crystalreach Islands Demo
[2025-08-31 14:02:01] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:02] [INFO] - (35/100) Processing AppID 1625150: MIA
[2025-08-31 14:02:03] [INFO] -    ✅ Found Game: MIA: SOS | Price: Free
[2025-08-31 14:02:04] [INFO] - (36/100) Processing AppID 2357550: AngelStrike
[2025-08-31 14:02:04] [INFO] -    ✅ Found Game: AngelStrike | Price: $13.99
[2025-08-31 14:02:06] [INFO] - (37/100) Processing AppID 2932030: Espire 1 - Sydney Sneakabouts Mission Pack
[2025-08-31 14:02:06] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:07] [INFO] - (37/100) Processing AppID 3287060: Zalera Spark Demo
[2025-08-31 14:02:07] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:09] [INFO] - (37/100) Processing AppID 863190: Gamer Sensei's Range Royale
[2025-08-31 14:02:09] [INFO] -    ✅ Found Game: Gamer Sensei's Range Royale | Price: $5.99
[2025-08-31 14:02:10] [INFO] - (38/100) Processing AppID 3653090: Fuga: Melodies of Steel (Manga) Vol. 7
[2025-08-31 14:02:11] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:12] [INFO] - (38/100) Processing AppID 1155910: Dice Defenders
[2025-08-31 14:02:12] [INFO] -    ✅ Found Game: Dice Defenders | Price: $4.99
[2025-08-31 14:02:12] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:02:14] [INFO] - (39/100) Processing AppID 1419220: Way Walkers: University 2 Demo
[2025-08-31 14:02:14] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:15] [INFO] - (39/100) Processing AppID 2299392: 選手テーマ：（ソフトバンク）「柳田悠岐選手のテーマ」
[2025-08-31 14:02:15] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:17] [INFO] - (39/100) Processing AppID 1811230: City of Gangsters: Atlantic City
[2025-08-31 14:02:17] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:19] [INFO] - (39/100) Processing AppID 2684230: Bubble Ball!
[2025-08-31 14:02:19] [INFO] -    ✅ Found Game: Bubble Ball! | Price: $2.99
[2025-08-31 14:02:20] [INFO] - (40/100) Processing AppID 1765160: 封神榜  伏魔三太子（重制版）
[2025-08-31 14:02:20] [INFO] -    ✅ Found Game: 封神榜  伏魔三太子（重制版） | Price: $7.99
[2025-08-31 14:02:22] [INFO] - (41/100) Processing AppID 3027170: Oil and Sand
[2025-08-31 14:02:22] [INFO] -    ✅ Found Game: Oil and Sand | Price: Free
[2025-08-31 14:02:23] [INFO] - (42/100) Processing AppID 1578123: Grass Cutters Academy - Space Age Cursor
[2025-08-31 14:02:23] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:25] [INFO] - (42/100) Processing AppID 978800: Rolling Bird
[2025-08-31 14:02:25] [INFO] -    ✅ Found Game: Rolling Bird | Price: $0.99
[2025-08-31 14:02:27] [INFO] - (43/100) Processing AppID 847415: Megadimension Neptunia VIIR - 4 Goddesses Online Adventurer Class Weapon Set
[2025-08-31 14:02:27] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:28] [INFO] - (43/100) Processing AppID 454610: Demon's Crystals
[2025-08-31 14:02:28] [INFO] -    ✅ Found Game: Demon's Crystals | Price: $2.99
[2025-08-31 14:02:30] [INFO] - (44/100) Processing AppID 1577802: Pixel Puzzles Illustrations & Anime - Jigsaw Pack: Egypt
[2025-08-31 14:02:30] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:31] [INFO] - (44/100) Processing AppID 1439840: Fright Night Sex Fest
[2025-08-31 14:02:32] [INFO] -    ✅ Found Game: Fright Night Sex Fest | Price: $9.99
[2025-08-31 14:02:33] [INFO] - (45/100) Processing AppID 2091230: Stories school
[2025-08-31 14:02:33] [INFO] -    ✅ Found Game: Stories school | Price: $1.29
[2025-08-31 14:02:35] [INFO] - (46/100) Processing AppID 1610080: RPG Maker VX Ace - Future Electric RPG Collection
[2025-08-31 14:02:35] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:36] [INFO] - (46/100) Processing AppID 1064460: Murder House
[2025-08-31 14:02:36] [INFO] -    ✅ Found Game: Murder House | Price: $11.99
[2025-08-31 14:02:38] [INFO] - (47/100) Processing AppID 1521500: AnyWay! - "Black kitten" Stickers Pack
[2025-08-31 14:02:38] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:39] [INFO] - (47/100) Processing AppID 2091170: Space Ballers Soundtrack
[2025-08-31 14:02:40] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:41] [INFO] - (47/100) Processing AppID 3536700: BeDo Demo
[2025-08-31 14:02:41] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:43] [INFO] - (47/100) Processing AppID 520600: Purrfect Date
[2025-08-31 14:02:43] [INFO] -    ✅ Found Game: Purrfect Date - Visual Novel/Dating Simulator | Price: $9.99
[2025-08-31 14:02:44] [INFO] - (48/100) Processing AppID 3474770: The Elder Scrolls Online: 2025 Content Pass Standard Upgrade Tracking
[2025-08-31 14:02:44] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:46] [INFO] - (48/100) Processing AppID 2019010: Flesh Everest
[2025-08-31 14:02:46] [INFO] -    ✅ Found Game: Flesh Everest | Price: Free
[2025-08-31 14:02:47] [INFO] - (49/100) Processing AppID 774342: SpaceSys - Formula Environment
[2025-08-31 14:02:48] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:49] [INFO] - (49/100) Processing AppID 1424160: Fuzz Force: Spook Squad Demo
[2025-08-31 14:02:49] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:51] [INFO] - (49/100) Processing AppID 1187220: Saturnalia Demo
[2025-08-31 14:02:51] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:52] [INFO] - (49/100) Processing AppID 2753600: Vambrace: Dungeon Monarch
[2025-08-31 14:02:52] [INFO] -    ✅ Found Game: Vambrace: Dungeon Monarch | Price: $14.99
[2025-08-31 14:02:52] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:02:54] [INFO] - (50/100) Processing AppID 2103440: SHIRIME 2: The Genesis of Butt-Eye
[2025-08-31 14:02:54] [INFO] -    ✅ Found Game: SHIRIME 2: The Genesis of Butt-Eye | Price: Free
[2025-08-31 14:02:55] [INFO] - (51/100) Processing AppID 794600: LET IT DIE
[2025-08-31 14:02:56] [INFO] -    ✅ Found Game: LET IT DIE | Price: Free
[2025-08-31 14:02:57] [INFO] - (52/100) Processing AppID 3136470: Fantasy Map Simulator Demo
[2025-08-31 14:02:57] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:02:59] [INFO] - (52/100) Processing AppID 1380820: Helixian
[2025-08-31 14:02:59] [INFO] -    ✅ Found Game: Helixian | Price: $1.99
[2025-08-31 14:03:00] [INFO] - (53/100) Processing AppID 4530: Full Spectrum Warrior: Ten Hammers
[2025-08-31 14:03:01] [INFO] -    ✅ Found Game: Full Spectrum Warrior: Ten Hammers | Price: $9.99
[2025-08-31 14:03:02] [INFO] - (54/100) Processing AppID 1404980: NENA
[2025-08-31 14:03:02] [INFO] -    ✅ Found Game: NENA | Price: Free
[2025-08-31 14:03:04] [INFO] - (55/100) Processing AppID 552690: Fantasy Fairways
[2025-08-31 14:03:04] [INFO] -    ✅ Found Game: Fantasy Fairways | Price: $6.99
[2025-08-31 14:03:05] [INFO] - (56/100) Processing AppID 2360390: Undead Space
[2025-08-31 14:03:05] [INFO] -    ✅ Found Game: Undead Space | Price: Free
[2025-08-31 14:03:07] [INFO] - (57/100) Processing AppID 2801100: RPG Maker MZ - Jewels Asset Pack 4K
[2025-08-31 14:03:07] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:08] [INFO] - (57/100) Processing AppID 300220: Victim of Xen
[2025-08-31 14:03:09] [INFO] -    ✅ Found Game: Victim of Xen | Price: $9.99
[2025-08-31 14:03:10] [INFO] - (58/100) Processing AppID 3529280: Talented - Supporter Pack
[2025-08-31 14:03:10] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:12] [INFO] - (58/100) Processing AppID 711680: Dungeons 3 - Evil of the Caribbean
[2025-08-31 14:03:12] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:13] [INFO] - (58/100) Processing AppID 671382: Red Bull 360: Take part in the fastest sport on skates
[2025-08-31 14:03:13] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:15] [INFO] - (58/100) Processing AppID 389922: Fantasy Grounds - Top-Down Tokens - More Monsters 2
[2025-08-31 14:03:15] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:16] [INFO] - (58/100) Processing AppID 609440: Peace, Death! - Soundtrack
[2025-08-31 14:03:17] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:18] [INFO] - (58/100) Processing AppID 1469580: Fantasy Grounds - Pathfinder RPG - Campaign Setting: Inner Sea NPC Codex
[2025-08-31 14:03:18] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:20] [INFO] - (58/100) Processing AppID 1959060: Schrodinger's Catgirl Demo
[2025-08-31 14:03:20] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:21] [INFO] - (58/100) Processing AppID 1262423: The Legend of Heroes: Trails of Cold Steel III  - Musse's "Coquettish Blue" Costume
[2025-08-31 14:03:21] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:23] [INFO] - (58/100) Processing AppID 390419: Rocksmith 2014 - Wolfmother - Woman
[2025-08-31 14:03:23] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:25] [INFO] - (58/100) Processing AppID 957290: Ales Dash - Soundtrack
[2025-08-31 14:03:25] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:26] [INFO] - (58/100) Processing AppID 2929840: Dreams and bubbles
[2025-08-31 14:03:26] [INFO] -    ✅ Found Game: Dreams and bubbles | Price: $29.99
[2025-08-31 14:03:28] [INFO] - (59/100) Processing AppID 3425060: Fantasy Quest Realm Survival
[2025-08-31 14:03:28] [INFO] -    ✅ Found Game: Fantasy Quest Realm Survival | Price: $0.99
[2025-08-31 14:03:29] [INFO] - (60/100) Processing AppID 1024850: Flow Weaver
[2025-08-31 14:03:29] [INFO] -    ✅ Found Game: Flow Weaver | Price: $19.99
[2025-08-31 14:03:31] [INFO] - (61/100) Processing AppID 2203210: BURGGEIST
[2025-08-31 14:03:31] [INFO] -    ✅ Found Game: BURGGEIST | Price: $12.00
[2025-08-31 14:03:33] [INFO] - (62/100) Processing AppID 628060: Romance of the Three Kingdoms X with Power Up Kit
[2025-08-31 14:03:33] [INFO] -    ✅ Found Game: Romance of the Three Kingdoms X with Power Up Kit | Price: $29.99
[2025-08-31 14:03:33] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:03:34] [INFO] - (63/100) Processing AppID 2559690: Draco and the Seven Scales
[2025-08-31 14:03:34] [INFO] -    ✅ Found Game: Draco and the Seven Scales | Price: Free
[2025-08-31 14:03:36] [INFO] - (64/100) Processing AppID 2278780: Cats in Heat - Summer Fling
[2025-08-31 14:03:36] [INFO] -    ✅ Found Game: Cats in Heat - Summer Fling | Price: $2.09
[2025-08-31 14:03:37] [INFO] - (65/100) Processing AppID 804640: BBTAG DLC Character - Blake
[2025-08-31 14:03:38] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:39] [INFO] - (65/100) Processing AppID 1570340: Dawn of the Falkonir
[2025-08-31 14:03:39] [INFO] -    ✅ Found Game: Dawn of the Falkonir | Price: Free
[2025-08-31 14:03:41] [INFO] - (66/100) Processing AppID 3641140: Call of Duty®: Modern Warfare® II - Desert Rogue: Pro-pack
[2025-08-31 14:03:41] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:42] [INFO] - (66/100) Processing AppID 2684280: 水箱
[2025-08-31 14:03:42] [INFO] -    ✅ Found Game: 水箱 | Price: $1.99
[2025-08-31 14:03:44] [INFO] - (67/100) Processing AppID 2490010: From_. Demo
[2025-08-31 14:03:44] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:45] [INFO] - (67/100) Processing AppID 3564630: 领星物语-感谢有你-1
[2025-08-31 14:03:46] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:47] [INFO] - (67/100) Processing AppID 2499400: Dragon Ranch
[2025-08-31 14:03:47] [INFO] -    ✅ Found Game: Dragon Ranch | Price: Free
[2025-08-31 14:03:49] [INFO] - (68/100) Processing AppID 1685090: RPG Maker MZ - MT Terrains
[2025-08-31 14:03:49] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:50] [INFO] - (68/100) Processing AppID 2003600: Don't Stop the Camera! ~Hidden Desires of a Young Wife~
[2025-08-31 14:03:50] [INFO] -    ✅ Found Game: Don't Stop the Camera! ~Hidden Desires of a Young Wife~ | Price: $13.99
[2025-08-31 14:03:52] [INFO] - (69/100) Processing AppID 1434290: Fantasy Grounds - Pathfinder RPG - Campaign Setting: The Inner Sea World Guide
[2025-08-31 14:03:52] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:53] [INFO] - (69/100) Processing AppID 555790: Fantasy Grounds - Lankhmar: City of Thieves (Savage Worlds)
[2025-08-31 14:03:54] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:55] [INFO] - (69/100) Processing AppID 1341990: Half-Life 2: Genry's Great Escape From City 13 Demo
[2025-08-31 14:03:55] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:57] [INFO] - (69/100) Processing AppID 1624290: Half-Life: A Place in the West - Chapter 7
[2025-08-31 14:03:57] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:03:58] [INFO] - (69/100) Processing AppID 418180: Tempest
[2025-08-31 14:03:58] [INFO] -    ✅ Found Game: Tempest: Pirate Action RPG | Price: $14.99
[2025-08-31 14:04:00] [INFO] - (70/100) Processing AppID 2397350: Castlewatch Playtest
[2025-08-31 14:04:00] [INFO] -    ✅ Found Game: Castlewatch Playtest | Price: Free
[2025-08-31 14:04:01] [INFO] - (71/100) Processing AppID 2574210: RPG Maker MV - Doomsday Music Pack Vol 2
[2025-08-31 14:04:02] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:03] [INFO] - (71/100) Processing AppID 1338140: Meditation Journey: VR Zen Garden
[2025-08-31 14:04:03] [INFO] -    ✅ Found Game: VR Zen Garden & ASMR Playground | Price: $14.99
[2025-08-31 14:04:05] [INFO] - (72/100) Processing AppID 3227500: Blades of Mirage
[2025-08-31 14:04:05] [INFO] -    ✅ Found Game: Blades of Mirage | Price: Free
[2025-08-31 14:04:06] [INFO] - (73/100) Processing AppID 2011650: Spiritus
[2025-08-31 14:04:06] [INFO] -    ✅ Found Game: SPIRITUS | Price: $7.99
[2025-08-31 14:04:08] [INFO] - (74/100) Processing AppID 81254: Take on Helicopters - Launch Trailer
[2025-08-31 14:04:08] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:10] [INFO] - (74/100) Processing AppID 2279610: House of Lies
[2025-08-31 14:04:10] [INFO] -    ✅ Found Game: House of Lies | Price: Free
[2025-08-31 14:04:11] [INFO] - (75/100) Processing AppID 740710: Expansion Content
[2025-08-31 14:04:11] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:13] [INFO] - (75/100) Processing AppID 1047480: Miner Lou
[2025-08-31 14:04:13] [INFO] -    ✅ Found Game: Miner Lou | Price: Free
[2025-08-31 14:04:13] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:04:14] [INFO] - (76/100) Processing AppID 1161320: 东方幻昼梦~ Touhou Fantasy Day
[2025-08-31 14:04:14] [INFO] -    ✅ Found Game: 东方幻昼梦~ Touhou Fantasy Day | Price: $1.99
[2025-08-31 14:04:16] [INFO] - (77/100) Processing AppID 2245690: Islands & Trains Demo
[2025-08-31 14:04:16] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:18] [INFO] - (77/100) Processing AppID 1564290: 空梦 Demo
[2025-08-31 14:04:18] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:19] [INFO] - (77/100) Processing AppID 1460320: Bountiful Life Demo
[2025-08-31 14:04:19] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:21] [INFO] - (77/100) Processing AppID 81412: 1000 Amps Trailer
[2025-08-31 14:04:21] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:23] [INFO] - (77/100) Processing AppID 2629780: Jigsaw-Land Demo
[2025-08-31 14:04:23] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:24] [INFO] - (77/100) Processing AppID 2780000: Chrono Ark - Summer Twilight
[2025-08-31 14:04:24] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:26] [INFO] - (77/100) Processing AppID 22610: Alien Breed: Impact
[2025-08-31 14:04:26] [INFO] -    ✅ Found Game: Alien Breed: Impact | Price: $1.99
[2025-08-31 14:04:27] [INFO] - (78/100) Processing AppID 2677670: Horny Holiday
[2025-08-31 14:04:27] [INFO] -    ✅ Found Game: Horny Holiday | Price: $4.99
[2025-08-31 14:04:29] [INFO] - (79/100) Processing AppID 1566700: VR Prison Escape
[2025-08-31 14:04:29] [INFO] -    ✅ Found Game: VR Prison Escape | Price: $1.99
[2025-08-31 14:04:31] [INFO] - (80/100) Processing AppID 1105790: Fantasy Grounds - Starfinder RPG - Signal of Screams AP 1: The Diaspora Strain (SFRPG
[2025-08-31 14:04:31] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:32] [INFO] - (80/100) Processing AppID 907410: Hard Times
[2025-08-31 14:04:32] [INFO] -    ✅ Found Game: Hard Times | Price: Free
[2025-08-31 14:04:34] [INFO] - (81/100) Processing AppID 2949580: 琉隐九绝
[2025-08-31 14:04:34] [INFO] -    ✅ Found Game: Nine Treasures of Liuyin | Price: $18.99
[2025-08-31 14:04:35] [INFO] - (82/100) Processing AppID 2058200: Showrunner
[2025-08-31 14:04:35] [INFO] -    ✅ Found Game: Showrunner | Price: $8.99
[2025-08-31 14:04:37] [INFO] - (83/100) Processing AppID 992880: Space Cruise
[2025-08-31 14:04:37] [INFO] -    ✅ Found Game: Space Cruise | Price: $8.00
[2025-08-31 14:04:39] [INFO] - (84/100) Processing AppID 1988810: BCI Horror Attraction
[2025-08-31 14:04:39] [INFO] -    ✅ Found Game: BCI VR Horror Attraction: The Mad Trail | Price: Free
[2025-08-31 14:04:40] [INFO] - (85/100) Processing AppID 3249320: Strangler
[2025-08-31 14:04:40] [INFO] -    ✅ Found Game: Strangler | Price: $3.99
[2025-08-31 14:04:42] [INFO] - (86/100) Processing AppID 1372430: Spells and Fellas
[2025-08-31 14:04:42] [INFO] -    ✅ Found Game: Spells and Fellas | Price: Free
[2025-08-31 14:04:43] [INFO] - (87/100) Processing AppID 2755950: Tidebound
[2025-08-31 14:04:44] [INFO] -    ✅ Found Game: Tidebound | Price: Free
[2025-08-31 14:04:45] [INFO] - (88/100) Processing AppID 3041860: Ninjabun Demo
[2025-08-31 14:04:45] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:47] [INFO] - (88/100) Processing AppID 3616480: Grimdelve
[2025-08-31 14:04:47] [INFO] -    ✅ Found Game: Grimdelve | Price: Free
[2025-08-31 14:04:48] [INFO] - (89/100) Processing AppID 3089280: Digital Humans
[2025-08-31 14:04:48] [INFO] -    ✅ Found Game: Digital Humans | Price: $18.99
[2025-08-31 14:04:50] [INFO] - (90/100) Processing AppID 2850260: ELHKIA
[2025-08-31 14:04:50] [INFO] -    ✅ Found Game: ELHKIA | Price: Free
[2025-08-31 14:04:51] [INFO] - (91/100) Processing AppID 2600480: Whisper in the Dark
[2025-08-31 14:04:52] [INFO] -    ✅ Found Game: Whisper: in the Dark | Price: Free
[2025-08-31 14:04:53] [INFO] - (92/100) Processing AppID 1244560: Outward Soundtrack
[2025-08-31 14:04:53] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:53] [INFO] - 💾 Performing periodic save...
[2025-08-31 14:04:55] [INFO] - (92/100) Processing AppID 967450: Special Counter Force Attack
[2025-08-31 14:04:55] [INFO] -    ✅ Found Game: Special Counter Force Attack | Price: $4.99
[2025-08-31 14:04:56] [INFO] - (93/100) Processing AppID 1752110: Growbot Soundtrack
[2025-08-31 14:04:56] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:04:58] [INFO] - (93/100) Processing AppID 2241200: Dyztopia: Post-Human RPG
[2025-08-31 14:04:58] [INFO] -    ✅ Found Game: Dyztopia: Post-Human RPG | Price: $9.99
[2025-08-31 14:05:00] [INFO] - (94/100) Processing AppID 1197650: Barotrauma - Supporter Pack
[2025-08-31 14:05:00] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:01] [INFO] - (94/100) Processing AppID 1813880: Elemental War 2 Demo
[2025-08-31 14:05:01] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:03] [INFO] - (94/100) Processing AppID 3939550: Sunset Street Ninja
[2025-08-31 14:05:03] [INFO] -    ✅ Found Game: Sunset Street Ninja | Price: Free
[2025-08-31 14:05:04] [INFO] - (95/100) Processing AppID 2010950: 后汉稽异录～测试版
[2025-08-31 14:05:04] [INFO] -    ✅ Found Game: Obscure Annals of Dynasty Playtest | Price: Free
[2025-08-31 14:05:06] [INFO] - (96/100) Processing AppID 1699090: Fomalhaut Flowers Demo
[2025-08-31 14:05:06] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:08] [INFO] - (96/100) Processing AppID 2368608: BGC_N_I_002_4
[2025-08-31 14:05:08] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:09] [INFO] - (96/100) Processing AppID 3758400: Coin Factory 2
[2025-08-31 14:05:09] [INFO] -    ✅ Found Game: Coin Factory 2 | Price: Free
[2025-08-31 14:05:11] [INFO] - (97/100) Processing AppID 2685820: Fantasy Adventure Builder - Premium Version Upgrade
[2025-08-31 14:05:11] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:12] [INFO] - (97/100) Processing AppID 2690960: Piece Link
[2025-08-31 14:05:12] [INFO] -    ✅ Found Game: Piece Link | Price: $0.99
[2025-08-31 14:05:14] [INFO] - (98/100) Processing AppID 3031950: YouthSignal Demo
[2025-08-31 14:05:14] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:16] [INFO] - (98/100) Processing AppID 3413570: DirtyLeague - Holiday Special Pack
[2025-08-31 14:05:16] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:17] [INFO] - (98/100) Processing AppID 627040: The Dark Tapes
[2025-08-31 14:05:17] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:19] [INFO] - (98/100) Processing AppID 869460: Lame & Cheesy
[2025-08-31 14:05:19] [INFO] -    ✅ Found Game: The Experimental Adventures of Lame & Cheesy | Price: Free
[2025-08-31 14:05:20] [INFO] - (99/100) Processing AppID 3780340: Everlusting Life - Mascot Marylin
[2025-08-31 14:05:20] [WARNING] -    - Skipped: Not a valid game or details failed.
[2025-08-31 14:05:22] [INFO] - (99/100) Processing AppID 899440: GOD EATER 3
[2025-08-31 14:05:22] [INFO] -    ✅ Found Game: GOD EATER 3 | Price: $59.99
[2025-08-31 14:05:24] [INFO] - 💾 Performing final save...
[2025-08-31 14:05:24] [INFO] - 🎉 Collection complete!
[2025-08-31 14:05:24] [INFO] -    Target Games: 100
[2025-08-31 14:05:24] [INFO] -    Actual Games Found: 100
[2025-08-31 14:05:24] [INFO] -    Total Apps Processed: 193
[2025-08-31 14:05:24] [INFO] -    Data saved to steam_data_sample.json```
