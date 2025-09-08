# Steam API Data Schema Analysis Report

## 1. Dataset Summary

| Metric                             | Value |
| :----------------------------------- | :---- |
| Total Records Analyzed | 193 |
| Records with Successful API Details | 170 (88.1%) |
| Records Identified as 'Game' | 100 (51.8%) |
| Free Games | 35 (35.0%) |

## 2. Field Analysis & PostgreSQL Schema Recommendation

This table details every field discovered in the dataset.

- Presence: How often the field appeared across all analyzed records.
- Data Types: The Python data types observed for this field.
- Recommended PG Type: A suggested PostgreSQL column type. `JSONB` is recommended for any nested or array structures.

| Field Path (Dot Notation) | Presence | Non-Null | Data Types | Recommended PG Type | Notes / Examples |
| :-------------------------- | :------- | :------- | :--------- | :------------------ | :--------------- |
| `app_details` | 100.0% | 100.0% | dict | JSONB |  |
| `app_details.appid` | 100.0% | 100.0% | int | BIGINT | 2267870, 2713920, 3210840 |
| `app_details.data` | 88.1% | 100.0% | dict | JSONB |  |
| `app_details.data.about_the_game` | 88.1% | 92.9% | str | TEXT | <p class="bb_paragraph" >Ninja Numpties is a video board game where 2-4 players place traps on a mini Chess board island, but watch out – the traps disappear next turn! Earn ninja stars by pranking your frenemies... Whoever has the most stars by the end of the game wins!</p><h2 class="bb_tag" >Three distinct kinds of traps!</h2><ul class="bb_ul"><li><p class="bb_paragraph" ><strong>Push Tiles </strong>drag your foes around or even off the island! Daisy-chain them to form a conveyor belt!</p></li><li><p class="bb_paragraph" ><strong>D4 Caltrops</strong> deal damage to your (opponent’s) dice roll!</p></li><li><p class="bb_paragraph" ><strong>Rock-Paper-Scissors</strong> traps start the RPS minigame! The winner gets at least 1 star – raise the stakes by making a Push Tile path to the rock/paper/scissors...</p></li></ul><h2 class="bb_tag" >Press P to pause, not Escape!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Ninja Numpties is a Game Maker 8.0 game so the Escape key instantly closes it!</p></li><li><p class="bb_paragraph" ><strong>Autosave </strong>to the rescue! Return to where you left off before you “paused” the game...</p></li><li><p class="bb_paragraph" >Start button on gamepads will pause the game as usual.</p></li></ul><h2 class="bb_tag" >Adjust match settings!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Set number of rounds to adjust the length of the play session (game autosaves, so feel free to continue a long session later...)</p></li><li><p class="bb_paragraph" >Individually adjust the <strong>first d6 roll </strong>and <strong>all subsequent d6 rolls...</strong> (random or fixed value)</p></li><li><p class="bb_paragraph" >Set d4 caltrop damage (Random, fixed value, or even Push Tile conveyor combo!)</p></li><li><p class="bb_paragraph" >Wrong settings? Pause the game (with <strong>P key</strong>) to revisit the Settings menu!</p></li></ul><h2 class="bb_tag" >Supports a wide range of gamepads and even shows their buttons!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >PlayStation DualShock 3/4 and DualSense</p></li><li><p class="bb_paragraph" >Xbox 360, One and Series S | X</p></li><li><p class="bb_paragraph" >Nintendo Switch Joy-Con (individually) and Pro controllers</p></li><li><p class="bb_paragraph" >NES, SNES (Purple and Multicolour), Gamecube controller and Wii Nunchuck</p></li><li><p class="bb_paragraph" >uDraw tablet (PlayStation 3 model)</p></li></ul><h2 class="bb_tag" >Choc-a-bloc full of memes and puns!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Licensed Vine boom and Kill Bill guitar riff (“rizz sound”)</p></li><li><p class="bb_paragraph" >Silly puns such as earning stars (badum tuss!)</p></li><li><p class="bb_paragraph" >Badly drawn memes!</p></li></ul>, <h2 class="bb_tag" >Welcome to Stewart the Fox!⠀</h2><p class="bb_paragraph" ></p><p class="bb_paragraph" >in this action-packed platformer, you'll play as Stewart, a brave fox on a quest to defeat enemies, overcome obstacles, and emerge victorious.⠀</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >As you journey through the game's four levels, you'll encounter a variety of challenges and foes, including tricky jumps, dangerous enemies and two epic boss battles. With quick reflexes and clever strategy, you'll need to navigate through each level and emerge unscathed.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >But the challenges don't stop there! Throughout the game, you'll also be on the lookout for collectibles hidden throughout the levels.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >So grab your controller / mouse and join Stewart on his epic adventure. Can you help him emerge victorious and claim victory in Stewart the Fox?</p><p class="bb_paragraph" ></p><h2 class="bb_tag" >Play the new Multiplayer mode!</h2><p class="bb_paragraph" >Speedrun through the levels with up to 5 other friends! click the Multiplayer button in the main menu to play online.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" ><strong>NOTE: This game is meant to be challenging depending on your Platformer skills. (This means that some people may have alot of trouble beating the game, is this the case for you? Visit the #Guides section in the community tab to view a Developer playtrough!</strong></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ><strong>NOTE: Controllers are supported in-game, not in Menu's.</strong></p><p class="bb_paragraph" ><strong>NOTE: This game is made by a single developer in the timespan of 2 weeks, keep this in mind, its meant to be a fun little game to speedrun or beat.</strong></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ></p>, Where's the Boat is a sandbox open world survival crafting game set on an archipelago of deserted islands. Explore randomly generated islands littered with man made trash. Uncover secrets, ancient treasure and magical creatures while trying to survive.<h2 class="bb_tag" >Current features:</h2>*Around 20 randomly generated islands<br>* Day/night cycle<br>*Changing seasons<br>* 5 different biomes<br>*Simulation of plants and animals<br>* Item/tool crafting<br>*Building structures<br>* Sailing<br>* Basic needs and afflictions |
| `app_details.data.achievements` | 21.2% | 100.0% | dict | JSONB |  |
| `app_details.data.achievements.highlighted` | 20.7% | 100.0% | list | JSONB |  |
| `app_details.data.achievements.highlighted[*].name` | 20.7% | 100.0% | str | TEXT | Storms Ahead, Let's You and Me Have A Little Talk, Friend, Finished Level 1 |
| `app_details.data.achievements.highlighted[*].path` | 20.7% | 100.0% | str | TEXT | <https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/262000/f2989d9c5a75680761f8313825e0cd4dc75c94d9.jpg>, <https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/2860620/7a4be1e1c9c6e4f4a102135fd6a45760d9f64da2.jpg>, <https://cdn.akamai.steamstatic.com/steamcommunity/public/images/apps/2267870/b2a2ec90d825e6c0546f11c4647fb64fd5eace9e.jpg> |
| `app_details.data.achievements.total` | 21.2% | 100.0% | int | BIGINT | 17, 51, 19 |
| `app_details.data.background` | 88.1% | 100.0% | str | TEXT | <https://store.akamai.steamstatic.com/images/storepagebackground/app/2713920?t=1717630275>, <https://store.akamai.steamstatic.com/images/storepagebackground/app/3210840?t=1733778902>, <https://store.akamai.steamstatic.com/images/storepagebackground/app/2267870?t=1750754633> |
| `app_details.data.background_raw` | 88.1% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/page_bg_raw.jpg?t=1717630275>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/page_bg_raw.jpg?t=1733778902>, <https://store.akamai.steamstatic.com/images/storepagebackground/app/2267870?t=1750754633> |
| `app_details.data.capsule_image` | 88.1% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2267870/1740db35da98edd194f5c1ef8bf8d5ba139ea620/capsule_231x87.jpg?t=1750754633>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/287e9781debe2ffbc821a0d1d476b55e6c0ad75a/capsule_231x87.jpg?t=1733778902>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/capsule_231x87.jpg?t=1717630275> |
| `app_details.data.capsule_imagev5` | 88.1% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/287e9781debe2ffbc821a0d1d476b55e6c0ad75a/capsule_184x69.jpg?t=1733778902>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2267870/1740db35da98edd194f5c1ef8bf8d5ba139ea620/capsule_184x69.jpg?t=1750754633>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/capsule_184x69.jpg?t=1717630275> |
| `app_details.data.categories` | 81.9% | 100.0% | list | JSONB |  |
| `app_details.data.categories[*].description` | 81.9% | 100.0% | str | TEXT | Multi-player, Single-player, Family Sharing |
| `app_details.data.categories[*].id` | 81.9% | 100.0% | int | BIGINT | 1, 62, 2 |
| `app_details.data.content_descriptors` | 88.1% | 100.0% | dict | JSONB |  |
| `app_details.data.content_descriptors.ids` | 88.1% | 21.8% | list | JSONB |  |
| `app_details.data.content_descriptors.notes` | 88.1% | 16.5% | NoneType, str | TEXT | This Game may contain content not appropriate for all ages, or may not be appropriate for viewing at work: Nudity or Sexual Content, Adult Only Sexual Content, General Mature Content, Contains foot and tickling fetish content., Depictions of alcohol, firearms, violence, blood. |
| `app_details.data.controller_support` | 22.8% | 100.0% | str | TEXT | full |
| `app_details.data.demos` | 7.8% | 100.0% | list | JSONB |  |
| `app_details.data.demos[*].appid` | 7.8% | 100.0% | int | BIGINT | 3279290, 2628520, 318170 |
| `app_details.data.demos[*].description` | 7.8% | 6.7% | str | TEXT | Free |
| `app_details.data.detailed_description` | 88.1% | 92.9% | str | TEXT | <p class="bb_paragraph" >Ninja Numpties is a video board game where 2-4 players place traps on a mini Chess board island, but watch out – the traps disappear next turn! Earn ninja stars by pranking your frenemies... Whoever has the most stars by the end of the game wins!</p><h2 class="bb_tag" >Three distinct kinds of traps!</h2><ul class="bb_ul"><li><p class="bb_paragraph" ><strong>Push Tiles </strong>drag your foes around or even off the island! Daisy-chain them to form a conveyor belt!</p></li><li><p class="bb_paragraph" ><strong>D4 Caltrops</strong> deal damage to your (opponent’s) dice roll!</p></li><li><p class="bb_paragraph" ><strong>Rock-Paper-Scissors</strong> traps start the RPS minigame! The winner gets at least 1 star – raise the stakes by making a Push Tile path to the rock/paper/scissors...</p></li></ul><h2 class="bb_tag" >Press P to pause, not Escape!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Ninja Numpties is a Game Maker 8.0 game so the Escape key instantly closes it!</p></li><li><p class="bb_paragraph" ><strong>Autosave </strong>to the rescue! Return to where you left off before you “paused” the game...</p></li><li><p class="bb_paragraph" >Start button on gamepads will pause the game as usual.</p></li></ul><h2 class="bb_tag" >Adjust match settings!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Set number of rounds to adjust the length of the play session (game autosaves, so feel free to continue a long session later...)</p></li><li><p class="bb_paragraph" >Individually adjust the <strong>first d6 roll </strong>and <strong>all subsequent d6 rolls...</strong> (random or fixed value)</p></li><li><p class="bb_paragraph" >Set d4 caltrop damage (Random, fixed value, or even Push Tile conveyor combo!)</p></li><li><p class="bb_paragraph" >Wrong settings? Pause the game (with <strong>P key</strong>) to revisit the Settings menu!</p></li></ul><h2 class="bb_tag" >Supports a wide range of gamepads and even shows their buttons!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >PlayStation DualShock 3/4 and DualSense</p></li><li><p class="bb_paragraph" >Xbox 360, One and Series S | X</p></li><li><p class="bb_paragraph" >Nintendo Switch Joy-Con (individually) and Pro controllers</p></li><li><p class="bb_paragraph" >NES, SNES (Purple and Multicolour), Gamecube controller and Wii Nunchuck</p></li><li><p class="bb_paragraph" >uDraw tablet (PlayStation 3 model)</p></li></ul><h2 class="bb_tag" >Choc-a-bloc full of memes and puns!</h2><ul class="bb_ul"><li><p class="bb_paragraph" >Licensed Vine boom and Kill Bill guitar riff (“rizz sound”)</p></li><li><p class="bb_paragraph" >Silly puns such as earning stars (badum tuss!)</p></li><li><p class="bb_paragraph" >Badly drawn memes!</p></li></ul>, <h2 class="bb_tag" >Welcome to Stewart the Fox!⠀</h2><p class="bb_paragraph" ></p><p class="bb_paragraph" >in this action-packed platformer, you'll play as Stewart, a brave fox on a quest to defeat enemies, overcome obstacles, and emerge victorious.⠀</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >As you journey through the game's four levels, you'll encounter a variety of challenges and foes, including tricky jumps, dangerous enemies and two epic boss battles. With quick reflexes and clever strategy, you'll need to navigate through each level and emerge unscathed.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >But the challenges don't stop there! Throughout the game, you'll also be on the lookout for collectibles hidden throughout the levels.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" >So grab your controller / mouse and join Stewart on his epic adventure. Can you help him emerge victorious and claim victory in Stewart the Fox?</p><p class="bb_paragraph" ></p><h2 class="bb_tag" >Play the new Multiplayer mode!</h2><p class="bb_paragraph" >Speedrun through the levels with up to 5 other friends! click the Multiplayer button in the main menu to play online.</p><p class="bb_paragraph" ></p><p class="bb_paragraph" ><strong>NOTE: This game is meant to be challenging depending on your Platformer skills. (This means that some people may have alot of trouble beating the game, is this the case for you? Visit the #Guides section in the community tab to view a Developer playtrough!</strong></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ><strong>NOTE: Controllers are supported in-game, not in Menu's.</strong></p><p class="bb_paragraph" ><strong>NOTE: This game is made by a single developer in the timespan of 2 weeks, keep this in mind, its meant to be a fun little game to speedrun or beat.</strong></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ></p><p class="bb_paragraph" ></p>, Where's the Boat is a sandbox open world survival crafting game set on an archipelago of deserted islands. Explore randomly generated islands littered with man made trash. Uncover secrets, ancient treasure and magical creatures while trying to survive.<h2 class="bb_tag" >Current features:</h2>*Around 20 randomly generated islands<br>* Day/night cycle<br>*Changing seasons<br>* 5 different biomes<br>*Simulation of plants and animals<br>* Item/tool crafting<br>*Building structures<br>* Sailing<br>* Basic needs and afflictions |
| `app_details.data.developers` | 84.5% | 100.0% | list | JSONB |  |
| `app_details.data.dlc` | 6.7% | 100.0% | list | JSONB |  |
| `app_details.data.ext_user_account_notice` | 1.0% | 100.0% | str | TEXT | Google, Facebook, Apple, Hive , Gamer Sensei (Supports Linking to Steam Account) |
| `app_details.data.fullgame` | 35.8% | 100.0% | dict | JSONB |  |
| `app_details.data.fullgame.appid` | 35.8% | 100.0% | str | TEXT | 1052250, 24010, 2670940 |
| `app_details.data.fullgame.name` | 35.8% | 100.0% | str | TEXT | OhMyRace!, Tiger Tank 59 Ⅰ Black Hill Fortress, Train Simulator Classic 2024 |
| `app_details.data.genres` | 74.6% | 100.0% | list | JSONB |  |
| `app_details.data.genres[*].description` | 74.6% | 100.0% | str | TEXT | Adventure, Casual, Action |
| `app_details.data.genres[*].id` | 74.6% | 100.0% | str | TEXT | 1, 4, 25 |
| `app_details.data.header_image` | 88.1% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/header.jpg?t=1733778902>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2267870/dd173fba60d638129888f2ce46ceae90733a983a/header.jpg?t=1750754633>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/header.jpg?t=1717630275> |
| `app_details.data.is_free` | 88.1% | 100.0% | bool | BOOLEAN | False, True |
| `app_details.data.legal_notice` | 33.7% | 100.0% | str | TEXT | Music (c) Ninjabaka (CC-BY-SA 3.0)<br />
"Vine boom" used under license from Bluezone Corporation<br />
"Rizz sound" used under license from SoundDogs.com<br />
Art and voice acting by JJ H-E is marked with CC0 1.0, DB and the DB logo are trademarks of Deutsche Bahn AG. Southeastern is an exclusive copyright and mark of London & South Eastern Railway Ltd. All rights reserved. Used with Permission. Southern Pacific is a trademark, used under license. The Union Pacific shield is a trademark of the Union Pacific Railroad company . All other trademarks are the property of their respective owners., <strong>Developed by DeadEagle © <br>Published by Spitfire-Games™</strong> |
| `app_details.data.linux_requirements` | 88.1% | 37.1% | dict, list | JSONB |  |
| `app_details.data.linux_requirements.minimum` | 32.6% | 100.0% | str | TEXT | <strong>Minimum:</strong><br><ul class="bb_ul"></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li><strong>Additional Notes:</strong> System Supporting RPG Maker MV</li></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> SteamOS 1 or later<br></li><li><strong>Processor:</strong> 1GHz<br></li><li><strong>Memory:</strong> 32 MB RAM<br></li><li><strong>Graphics:</strong> 500MHz integrated graphics<br></li><li><strong>Storage:</strong> 40 MB available space<br></li><li><strong>Sound Card:</strong> DirectX 8 compatible<br></li><li><strong>VR Support:</strong> N/A<br></li><li><strong>Additional Notes:</strong> Ninja Numpties is a Windows executble, so it needs to run in Wine, Proton etc. Sound requires Proton 9.0 or later.</li></ul> |
| `app_details.data.linux_requirements.recommended` | 26.4% | 100.0% | str | TEXT | <strong>Recommended:</strong><br><ul class="bb_ul"></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> Any distribution<br></li><li><strong>Processor:</strong> 2 Ghz CPU<br></li><li><strong>Memory:</strong> 4 GB RAM<br></li><li><strong>Graphics:</strong> Drivers with support for OpenGL</li></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> Ubuntu 16.04.3 LTS + SteamOS (latest)<br></li><li><strong>Processor:</strong> Quad core 3.5 GHz or higher (Intel i5 4000 Series / AMD Ryzen 3 Series)<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> AMD/NVIDIA dedicated graphic card, with at least 3072MB of dedicated VRAM and with at least DirectX 11 and Shader Model 5.0 support (AMD R9 300 Series and NVIDIA GeForce GTX 900 Series or better)<br></li><li><strong>Storage:</strong> 5 GB available space<br></li><li><strong>Additional Notes:</strong> Other Linux distributions (Mint, etc.) MIGHT work but we cannot give official support for them</li></ul> |
| `app_details.data.mac_requirements` | 88.1% | 44.7% | dict, list | JSONB |  |
| `app_details.data.mac_requirements.minimum` | 39.4% | 100.0% | str | TEXT | <strong>Minimum:</strong><br><ul class="bb_ul"></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li><strong>Additional Notes:</strong> System Supporting RPG Maker MV</li></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> OX 10.6<br></li><li><strong>Processor:</strong> 2.4 GHz<br></li><li><strong>Memory:</strong> 2 GB RAM<br></li><li><strong>Graphics:</strong> 512 MB<br></li><li><strong>Storage:</strong> 4 GB available space<br></li><li><strong>Additional Notes:</strong> Minimum suggested screen resolution is 1024x768. Not recommended for play on Intel systems with integrated/shared video memory.</li></ul> |
| `app_details.data.mac_requirements.recommended` | 29.5% | 100.0% | str | TEXT | <strong>Recommended:</strong><br><ul class="bb_ul"></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> macOS 10.12 or newer (64-bit)<br></li><li><strong>Processor:</strong> 6th Generation Intel® Core™ i5 / Apple M1 or newer<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> NVIDIA® GeForce® GTX 970 or AMD equivalent<br></li><li><strong>Storage:</strong> 5 GB available space<br></li><li><strong>Additional Notes:</strong> Optimized for High settings / 60FPS @ 1080p</li></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> OSX 10.6 or later<br></li><li><strong>Processor:</strong> 2.4 GHz or higher<br></li><li><strong>Memory:</strong> 4 GB RAM<br></li><li><strong>Graphics:</strong> 1 GB or higher<br></li><li><strong>Storage:</strong> 4 GB available space<br></li><li><strong>Additional Notes:</strong> Not recommended for play on Intel systems with integrated/shared video memory.</li></ul> |
| `app_details.data.metacritic` | 4.1% | 100.0% | dict | JSONB |  |
| `app_details.data.metacritic.score` | 4.1% | 100.0% | int | BIGINT | 72, 70, 74 |
| `app_details.data.metacritic.url` | 4.1% | 100.0% | str | TEXT | <https://www.metacritic.com/game/pc/rollercoaster-tycoon-2?ftag=MCD-06-10aaa1f>, <https://www.metacritic.com/game/pc/purrfect-date?ftag=MCD-06-10aaa1f>, <https://www.metacritic.com/game/pc/gabriel-knight-sins-of-the-fathers-20th-anniversary-edition?ftag=MCD-06-10aaa1f> |
| `app_details.data.movies` | 49.2% | 100.0% | list | JSONB |  |
| `app_details.data.movies[*].highlight` | 49.2% | 100.0% | bool | BOOLEAN | True |
| `app_details.data.movies[*].id` | 49.2% | 100.0% | int | BIGINT | 256988261, 256923371, 257058420 |
| `app_details.data.movies[*].mp4` | 49.2% | 100.0% | dict | JSONB |  |
| `app_details.data.movies[*].mp4.480` | 49.2% | 100.0% | str | TEXT | <http://video.akamai.steamstatic.com/store_trailers/256988261/movie480.mp4?t=1702828108>, <http://video.akamai.steamstatic.com/store_trailers/257058420/movie480.mp4?t=1729284248>, <http://video.akamai.steamstatic.com/store_trailers/256923371/movie480.mp4?t=1698413665> |
| `app_details.data.movies[*].mp4.max` | 49.2% | 100.0% | str | TEXT | <http://video.akamai.steamstatic.com/store_trailers/256988261/movie_max.mp4?t=1702828108>, <http://video.akamai.steamstatic.com/store_trailers/256923371/movie_max.mp4?t=1698413665>, <http://video.akamai.steamstatic.com/store_trailers/257058420/movie_max.mp4?t=1729284248> |
| `app_details.data.movies[*].name` | 49.2% | 98.9% | str | TEXT | Video walkthrough (some boobytraps xD), Game Trailer, Stewart The Fox - Gameplay Trailer |
| `app_details.data.movies[*].thumbnail` | 49.2% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/256988261/movie.293x165.jpg?t=1702828108>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/256923371/movie.293x165.jpg?t=1698413665>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/257058420/movie.293x165.jpg?t=1729284248> |
| `app_details.data.movies[*].webm` | 49.2% | 100.0% | dict | JSONB |  |
| `app_details.data.movies[*].webm.480` | 49.2% | 100.0% | str | TEXT | <http://video.akamai.steamstatic.com/store_trailers/256923371/movie480_vp9.webm?t=1698413665>, <http://video.akamai.steamstatic.com/store_trailers/257058420/movie480_vp9.webm?t=1729284248>, <http://video.akamai.steamstatic.com/store_trailers/256988261/movie480_vp9.webm?t=1702828108> |
| `app_details.data.movies[*].webm.max` | 49.2% | 100.0% | str | TEXT | <http://video.akamai.steamstatic.com/store_trailers/256923371/movie_max_vp9.webm?t=1698413665>, <http://video.akamai.steamstatic.com/store_trailers/256988261/movie_max_vp9.webm?t=1702828108>, <http://video.akamai.steamstatic.com/store_trailers/257058420/movie_max_vp9.webm?t=1729284248> |
| `app_details.data.name` | 88.1% | 100.0% | str | TEXT | Stewart The Fox, Where's the Boat, Ninja Numpties |
| `app_details.data.package_groups` | 88.1% | 63.5% | list | JSONB |  |
| `app_details.data.package_groups[*].description` | 56.0% | 0.0% | str | TEXT |  |
| `app_details.data.package_groups[*].display_type` | 56.0% | 100.0% | int | BIGINT | 0 |
| `app_details.data.package_groups[*].is_recurring_subscription` | 56.0% | 100.0% | str | TEXT | false |
| `app_details.data.package_groups[*].name` | 56.0% | 100.0% | str | TEXT | default |
| `app_details.data.package_groups[*].save_text` | 56.0% | 0.0% | str | TEXT |  |
| `app_details.data.package_groups[*].selection_text` | 56.0% | 100.0% | str | TEXT | Select a purchase option |
| `app_details.data.package_groups[*].subs` | 56.0% | 100.0% | list | JSONB |  |
| `app_details.data.package_groups[*].subs[*].can_get_free_license` | 56.0% | 100.0% | str | TEXT | 0 |
| `app_details.data.package_groups[*].subs[*].is_free_license` | 56.0% | 100.0% | bool | BOOLEAN | False, True |
| `app_details.data.package_groups[*].subs[*].option_description` | 56.0% | 0.0% | str | TEXT |  |
| `app_details.data.package_groups[*].subs[*].option_text` | 56.0% | 100.0% | str | TEXT | Where's the Boat - $11.99, Ninja Numpties - $2.99, Yellow Ballman - $3.99 |
| `app_details.data.package_groups[*].subs[*].packageid` | 56.0% | 100.0% | int | BIGINT | 971515, 592181, 1138403 |
| `app_details.data.package_groups[*].subs[*].percent_savings` | 56.0% | 100.0% | int | BIGINT | 0 |
| `app_details.data.package_groups[*].subs[*].percent_savings_text` | 56.0% | 100.0% | str | TEXT | -25% ,  , -82%  |
| `app_details.data.package_groups[*].subs[*].price_in_cents_with_discount` | 56.0% | 100.0% | int | BIGINT | 399, 299, 1199 |
| `app_details.data.package_groups[*].title` | 56.0% | 100.0% | str | TEXT | Buy Ninja Numpties, Buy Yellow Ballman, Buy Where's the Boat |
| `app_details.data.packages` | 56.5% | 100.0% | list | JSONB |  |
| `app_details.data.pc_requirements` | 88.1% | 91.2% | dict, list | JSONB |  |
| `app_details.data.pc_requirements.minimum` | 80.3% | 100.0% | str | TEXT | <strong>Minimum:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10<br></li><li><strong>Processor:</strong> 3+ GHz<br></li><li><strong>Memory:</strong> 2+ GB RAM<br></li><li><strong>Graphics:</strong> GeForce GTX 750 ti<br></li><li><strong>Storage:</strong> 100 MB available space</li></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li><strong>OS:</strong> Windows 2000 or later<br></li><li><strong>Processor:</strong> 1GHz<br></li><li><strong>Memory:</strong> 32 MB RAM<br></li><li><strong>Graphics:</strong> 500MHz integrated graphics<br></li><li><strong>DirectX:</strong> Version 8.0<br></li><li><strong>Storage:</strong> 40 MB available space<br></li><li><strong>Sound Card:</strong> DirectX 8 compatible<br></li><li><strong>VR Support:</strong> N/A<br></li><li><strong>Additional Notes:</strong> Ninja Numpties is a Game Maker 8.0 executable, so should run fine on devices made in 2004 or later.</li></ul>, <strong>Minimum:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10/11 (64bit)<br></li><li><strong>Processor:</strong> AMD / Intel CPU running at 2.8 GHz or higher (AMD Phenom II X4 925 or Intel i3-4130 or newer are recommended)<br></li><li><strong>Memory:</strong> 4 GB RAM<br></li><li><strong>Graphics:</strong> AMD/NVIDIA graphic card, with at least 2GB of dedicated VRAM and with at least DirectX 11 and Shader Model 5.1 support: AMD Radeon HD 7870 or NVIDIA GeForce GTX 760 or newer is recommended.<br></li><li><strong>DirectX:</strong> Version 11<br></li><li><strong>Storage:</strong> 1100 MB available space</li></ul> |
| `app_details.data.pc_requirements.recommended` | 45.6% | 100.0% | str | TEXT | <strong>Recommended:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system</li></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li>Requires a 64-bit processor and operating system<br></li><li><strong>OS:</strong> Windows 10/11 (64bit)<br></li><li><strong>Processor:</strong> AMD / Intel processor running at 3.5 GHz or higher (AMD FX-6300 series or Intel Core i3-8100 or newer is recommended).<br></li><li><strong>Memory:</strong> 8 GB RAM<br></li><li><strong>Graphics:</strong> AMD/NVIDIA dedicated graphic card, with at least 4GB of dedicated VRAM (or more) and with at least DirectX 11 and Shader Model 5.1 support: NVIDIA GeForce GTX 1050 Ti or AMD Radeon R9<br></li><li><strong>DirectX:</strong> Version 11<br></li><li><strong>Storage:</strong> 1100 MB available space</li></ul>, <strong>Recommended:</strong><br><ul class="bb_ul"><li><strong>OS *:</strong> Windows XP or later<br></li><li><strong>Processor:</strong> 2.0 GHz<br></li><li><strong>Memory:</strong> 4 GB RAM<br></li><li><strong>Graphics:</strong> ATI or NVidia with 1 GB RAM<br></li><li><strong>Storage:</strong> 4 GB available space<br></li><li><strong>Additional Notes:</strong> Not recommended for play on Intel systems with integrated/shared video memory.</li></ul> |
| `app_details.data.platforms` | 88.1% | 100.0% | dict | JSONB |  |
| `app_details.data.platforms.linux` | 88.1% | 100.0% | bool | BOOLEAN | False, True |
| `app_details.data.platforms.mac` | 88.1% | 100.0% | bool | BOOLEAN | False, True |
| `app_details.data.platforms.windows` | 88.1% | 100.0% | bool | BOOLEAN | True |
| `app_details.data.price_overview` | 55.4% | 100.0% | dict | JSONB |  |
| `app_details.data.price_overview.currency` | 55.4% | 100.0% | str | TEXT | USD |
| `app_details.data.price_overview.discount_percent` | 55.4% | 100.0% | int | BIGINT | 82, 25, 0 |
| `app_details.data.price_overview.final` | 55.4% | 100.0% | int | BIGINT | 399, 299, 1199 |
| `app_details.data.price_overview.final_formatted` | 55.4% | 100.0% | str | TEXT | $3.99, $2.99, $11.99 |
| `app_details.data.price_overview.initial` | 55.4% | 100.0% | int | BIGINT | 399, 299, 1199 |
| `app_details.data.price_overview.initial_formatted` | 55.4% | 8.4% | str | TEXT | $0.99, $4.99, $12.99 |
| `app_details.data.publishers` | 79.3% | 100.0% | list | JSONB |  |
| `app_details.data.ratings` | 88.1% | 77.6% | NoneType, dict | JSONB |  |
| `app_details.data.ratings.agcom` | 0.5% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.agcom.descriptors` | 0.5% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.agcom.rating` | 0.5% | 100.0% | str | TEXT | 16 |
| `app_details.data.ratings.bbfc` | 2.1% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.bbfc.descriptors` | 1.6% | 100.0% | str | TEXT | This game requires hand and eye coordination, logic processing and decision making. Parents are the most appropriate judge as to weather this game is appropriate for their child's skill level., Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, Bad Language |
| `app_details.data.ratings.bbfc.rating` | 1.0% | 100.0% | str | TEXT | 15, 12 |
| `app_details.data.ratings.bbfc.use_age_gate` | 0.5% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.cero` | 2.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.cero.descriptors` | 1.0% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, このゲームには、手と目の調整、論理処理、意思決定が必要です。このゲームが子供のスキルレベルに合っているかどうかを判断するには、親が最も適切な裁判官です。
Kono gēmu ni wa,-te to me no chōsei, ronri shori, ishi kettei ga hitsuyōdesu. Kono gēmu ga kodomo no sukiru reberu ni atte iru ka dō ka o handan suru ni wa, oya ga mottomo tekisetsuna saibankandesu. |
| `app_details.data.ratings.cero.rating` | 2.1% | 100.0% | str | TEXT | d, z, a |
| `app_details.data.ratings.cero.required_age` | 0.5% | 100.0% | str | TEXT | 18 |
| `app_details.data.ratings.cero.use_age_gate` | 0.5% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.crl` | 2.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.crl.descriptors` | 1.0% | 100.0% | str | TEXT | Эта игра требует координации рук и глаз, логической обработки и принятия решений. Родители являются наиболее подходящим судьей, поскольку погода соответствует этой игре, соответствующая уровню их ребенка.
Eta igra trebuyet koordinatsii ruk i glaz, logicheskoy obrabotki i prinyatiya resheniy. Roditeli yavlyayutsya naiboleye podkhodyashchim sud'yey, poskol'ku pogoda sootvetstvuyet etoy igre, sootvetstvuyushchaya urovnyu ikh rebenka., Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.crl.rating` | 2.1% | 100.0% | str | TEXT | 16, 12 |
| `app_details.data.ratings.csrr` | 1.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.csrr.descriptors` | 0.5% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.csrr.rating` | 1.6% | 100.0% | str | TEXT | C15 |
| `app_details.data.ratings.dejus` | 66.8% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.dejus.banned` | 46.1% | 100.0% | str | TEXT | 0 |
| `app_details.data.ratings.dejus.descriptors` | 60.1% | 70.7% | str | TEXT | Violência fantasiosa, Drogas ilícitas
Violência
Nudez, Violência |
| `app_details.data.ratings.dejus.rating` | 66.3% | 100.0% | str | TEXT | 10, l, 14 |
| `app_details.data.ratings.dejus.rating_generated` | 46.1% | 100.0% | str | TEXT | 1 |
| `app_details.data.ratings.dejus.required_age` | 58.0% | 100.0% | str | TEXT | 10, 14, 0 |
| `app_details.data.ratings.dejus.use_age_gate` | 58.0% | 100.0% | str | TEXT | true, 0 |
| `app_details.data.ratings.esrb` | 7.8% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.esrb.descriptors` | 6.2% | 100.0% | str | TEXT | Blood
Strong Language
Violence, Blood and Gore

Violence

Strong Language, Blood and Gore
Nudity
Strong Language
Use of Drugs |
| `app_details.data.ratings.esrb.display_online_notice` | 1.0% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.esrb.interactive_elements` | 0.5% | 100.0% | str | TEXT | Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.esrb.rating` | 7.3% | 100.0% | str | TEXT | t, e, m |
| `app_details.data.ratings.esrb.required_age` | 1.0% | 100.0% | str | TEXT | 17 |
| `app_details.data.ratings.esrb.use_age_gate` | 1.0% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.fpb` | 1.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.fpb.descriptors` | 0.5% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.fpb.rating` | 1.6% | 100.0% | str | TEXT | 16 |
| `app_details.data.ratings.kgrb` | 2.1% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.kgrb.descriptors` | 1.6% | 100.0% | str | TEXT | Sexual
Violence, Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, 이 게임에는 손과 눈의 조정, 논리 처리 및 의사 결정이 필요합니다. 부모님은이 게임이 자녀의 기술 수준에 적합한 지 날씨에 대해 가장 적절한 판사입니다.
i geim-eneun songwa nun-ui jojeong, nonli cheoli mich uisa gyeoljeong-i pil-yohabnida. bumonim-eun-i geim-i janyeoui gisul sujun-e jeoghabhan ji nalssie daehae gajang jeogjeolhan pansaibnida. |
| `app_details.data.ratings.kgrb.rating` | 1.6% | 100.0% | str | TEXT | 15 |
| `app_details.data.ratings.mda` | 1.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.mda.descriptors` | 0.5% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.mda.rating` | 1.6% | 100.0% | str | TEXT | AA16 |
| `app_details.data.ratings.nzoflc` | 2.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.nzoflc.descriptors` | 2.1% | 100.0% | str | TEXT | Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, Strong Violence
Blood and Gore
Online Interactivity, %NZoflcDescriptors% |
| `app_details.data.ratings.nzoflc.rating` | 1.6% | 100.0% | str | TEXT | r16, m, ma15 |
| `app_details.data.ratings.nzoflc.required_age` | 0.5% | 100.0% | str | TEXT | 15 |
| `app_details.data.ratings.nzoflc.use_age_gate` | 0.5% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.oflc` | 3.6% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.oflc.descriptors` | 3.1% | 100.0% | str | TEXT | %oflcDescriptors%, Strong Violence
Blood and Gore
Online Interactivity, Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet |
| `app_details.data.ratings.oflc.rating` | 2.6% | 100.0% | str | TEXT | m, ma15 |
| `app_details.data.ratings.oflc.required_age` | 0.5% | 100.0% | str | TEXT | 15 |
| `app_details.data.ratings.oflc.use_age_gate` | 0.5% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.pegi` | 5.2% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.pegi.descriptors` | 4.1% | 100.0% | str | TEXT | Violence
Bad Language, Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, Bad Language
Violence
In-Game Purchases |
| `app_details.data.ratings.pegi.rating` | 4.7% | 100.0% | str | TEXT | 16, 3, 18 |
| `app_details.data.ratings.pegi.required_age` | 1.6% | 100.0% | str | TEXT | 16, 12, 18 |
| `app_details.data.ratings.pegi.use_age_gate` | 1.0% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.steam_germany` | 55.4% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.steam_germany.banned` | 55.4% | 100.0% | str | TEXT | 1, 0 |
| `app_details.data.ratings.steam_germany.descriptors` | 55.4% | 63.6% | str | TEXT | Drastische Gewalt
Drogen
Sexuelle Andeutungen, Gewalt, Fantasy-Gewalt |
| `app_details.data.ratings.steam_germany.rating` | 55.4% | 100.0% | str | TEXT | 12, 0, 6 |
| `app_details.data.ratings.steam_germany.rating_generated` | 55.4% | 100.0% | str | TEXT | 1 |
| `app_details.data.ratings.steam_germany.required_age` | 55.4% | 100.0% | str | TEXT | 12, 0, 6 |
| `app_details.data.ratings.steam_germany.use_age_gate` | 55.4% | 100.0% | str | TEXT | 0 |
| `app_details.data.ratings.usk` | 5.7% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.usk.descriptors` | 2.1% | 100.0% | str | TEXT | Fantasy Violence
Suggestive Themes
Strong Language
Use of Alcohol
Use of Drugs
Comic Mischief, Blood
Strong Language
Violence
Users Interact
In-Game Purchases
Unrestricted Internet, Violence (Gewalt), Kriegsthematik |
| `app_details.data.ratings.usk.rating` | 5.2% | 100.0% | str | TEXT | 16, 0, 18 |
| `app_details.data.ratings.usk.rating_id` | 0.5% | 100.0% | str | TEXT | 15547/06 |
| `app_details.data.ratings.usk.required_age` | 0.5% | 100.0% | str | TEXT | 18 |
| `app_details.data.ratings.usk.use_age_gate` | 0.5% | 100.0% | str | TEXT | true |
| `app_details.data.ratings.video` | 0.5% | 100.0% | dict | JSONB |  |
| `app_details.data.ratings.video.descriptors` | 0.5% | 100.0% | str | TEXT | Adult Content
Adult Language
Graphic Violence |
| `app_details.data.recommendations` | 10.4% | 100.0% | dict | JSONB |  |
| `app_details.data.recommendations.total` | 10.4% | 100.0% | int | BIGINT | 284, 4753, 892 |
| `app_details.data.release_date` | 88.1% | 100.0% | dict | JSONB |  |
| `app_details.data.release_date.coming_soon` | 88.1% | 100.0% | bool | BOOLEAN | False, True |
| `app_details.data.release_date.date` | 88.1% | 100.0% | str | TEXT | Nov 1, 2024, Jan 20, 2023, Jan 5, 2024 |
| `app_details.data.required_age` | 88.1% | 100.0% | int, str | BIGINT | 0, 17 |
| `app_details.data.reviews` | 1.0% | 100.0% | str | TEXT | “Since a few days on Steam Greenlight, Radical Fiction's Hard Times was this year's DIY surprise.”<br>Everyeye<br><br>“We will put you to the test, in these Hard Times ...”<br>Vita Extra<br><br>“The difficulty of the homeless's life is well suited to the genre, and the authors' personal experience is the basis for a video game that wants to be mechanically playful but also wants to denounce the indifference of society towards a parallel and invisible world that attracts our attention only for matters of decorum and public order.”<br>WebTrek<br>, “Purrfect Date is not just for cat lovers, it's for those who love a game with mystery, personality and the heart of British comedy - something a bit bizarre.”<br>Eurogamer<br><br>“It's cute and funny and clever in ways I didn't expect, and far from the kitty-kissing experience I was braced for. There are feels here that hit out of the blue.”<br>Kotaku<br><br>“Purrfect Date takes the visual novel, dating simulator genre and takes it in a whole other direction. Not only does it take it in another direction, but it sells it without even a blink of an eye! It’s a game that knows what it is, embraces it and has so much fun doing it you can’t help but feel the same euphoria too!”<br>Hey Poor Player<br> |
| `app_details.data.screenshots` | 85.0% | 100.0% | list | JSONB |  |
| `app_details.data.screenshots[*].id` | 85.0% | 100.0% | int | BIGINT | 4, 0, 31 |
| `app_details.data.screenshots[*].path_full` | 85.0% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2267870/e033f9f679cf2b9f158f0065b512f9f22d8439f1/ss_e033f9f679cf2b9f158f0065b512f9f22d8439f1.1920x1080.jpg?t=1750754633>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/ss_f8a5548b9465d72c4619b47a49a10bce7ca75952.1920x1080.jpg?t=1733778902>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/ss_f80613b16761fdb6380c1715d416df65f05a327b.1920x1080.jpg?t=1717630275> |
| `app_details.data.screenshots[*].path_thumbnail` | 85.0% | 100.0% | str | TEXT | <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2713920/ss_f80613b16761fdb6380c1715d416df65f05a327b.600x338.jpg?t=1717630275>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/3210840/ss_f8a5548b9465d72c4619b47a49a10bce7ca75952.600x338.jpg?t=1733778902>, <https://shared.akamai.steamstatic.com/store_item_assets/steam/apps/2267870/e033f9f679cf2b9f158f0065b512f9f22d8439f1/ss_e033f9f679cf2b9f158f0065b512f9f22d8439f1.600x338.jpg?t=1750754633> |
| `app_details.data.short_description` | 88.1% | 94.1% | str | TEXT | Boobytrap a mini Chess board in this turn-based party game for 2 - 4 players!Works on Steam Deck!Only ~40Mb!, Where's the Boat is a sandbox open world survival crafting game set on an archipelago of deserted islands. Gather resources, craft tools, tend to your needs and travel from island to island in search for a way back to civilization., Join Stewart the Fox on an epic adventure through four challenging levels filled with obstacles, enemies, and two boss battles. As you collect hidden items to help Stewart emerge victorious in this action-packed platformer game. |
| `app_details.data.steam_appid` | 88.1% | 100.0% | int | BIGINT | 2267870, 2713920, 3210840 |
| `app_details.data.support_info` | 88.1% | 100.0% | dict | JSONB |  |
| `app_details.data.support_info.email` | 88.1% | 81.8% | str | TEXT | jjharrison(hyphen)eason(AT)hotmail(DOT)commercial, <eagle@spitfire-games.com>, <studioketa@gmail.com> |
| `app_details.data.support_info.url` | 88.1% | 49.4% | str | TEXT | <http://www.railsimulator.com/support.php>, <http://hunterssite.web.fc2.com/>, <https://www.spitfire-games.com> |
| `app_details.data.supported_languages` | 81.3% | 100.0% | str | TEXT | English, Japanese, English<strong>*</strong><br><strong>*</strong>languages with full audio support, English<strong>*</strong>, German, Spanish - Spain, Dutch, Spanish - Latin America, French, Portuguese - Brazil, Portuguese - Portugal, Italian, Japanese, Korean, Polish, Russian, Simplified Chinese, Turkish<br><strong>*</strong>languages with full audio support |
| `app_details.data.type` | 88.1% | 100.0% | str | TEXT | dlc, music, game |
| `app_details.data.website` | 88.1% | 42.9% | NoneType, str | TEXT | <www.gabrielknight20th.com>, <http://www.railsimulator.com>, <https://www.spitfire-games.com> |
| `app_details.fetched_at` | 100.0% | 100.0% | str | TEXT | 2025-08-31T14:00:16.352312, 2025-08-31T14:00:14.749533, 2025-08-31T14:00:13.066604 |
| `app_details.success` | 100.0% | 100.0% | bool | BOOLEAN | False, True |
| `appid` | 100.0% | 100.0% | int | BIGINT | 2267870, 2713920, 3210840 |
| `name_from_applist` | 100.0% | 100.0% | str | TEXT | Stewart The Fox, Where's the Boat, Ninja Numpties |
| `reviews` | 100.0% | 0.0% | NoneType | TEXT |  |

### Notes on PostgreSQL Schema

- Primary Key: `appid` is the clear candidate for a `PRIMARY KEY`.
- TEXT vs. VARCHAR: `TEXT` is used as a safe default for strings of unknown length. It has no performance penalty compared to `VARCHAR` in modern PostgreSQL.
- JSONB: This type is crucial. It stores JSON in a decomposed binary format, which allows it to be queried and indexed efficiently. Fields like `app_details.data` or `reviews` should be stored in a single `JSONB` column rather than flattening them into dozens of SQL columns.root@proj-dp01:/mnt/data/steam-dataset-refresh#
