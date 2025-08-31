# Steam API Test Suite: Run Summary & Log

## Run Summary

| Metric                | Value                                        |
| :-------------------- | :------------------------------------------- |
| **Generating Script** | `test_steam_api.py` (v1.2)                   |
| **Repository** | `https://github.com/vintagedon/steam-dataset-2025` |
| **Start Timestamp** | `2025-08-31 15:18:26`                        |
| **End Timestamp** | `2025-08-31 15:18:45`                        |
| **Duration** | 19 seconds                                   |
| **Parameters** | Default full test suite run                  |
| **Results** |                                              |
| _Final Status_        | Success                                      |
| _GetAppList Status_   | Success (`263,901` apps found)               |
| _Rate Limit Test_     | `10/10` successful requests                  |
| _Effective Rate_      | `40.9` requests/minute (with 1.5s delay)     |

---

## Script Output Log

```log
[2025-08-31 15:18:26] [INFO] - 🚀 Starting Steam API Test Suite
[2025-08-31 15:18:26] [INFO] - Testing ISteamApps/GetAppList...
[2025-08-31 15:18:27] [INFO] - ✅ GetAppList successful - Found 263,901 applications.
[2025-08-31 15:18:27] [INFO] -    Sample: 5 - Dedicated Server
[2025-08-31 15:18:27] [INFO] -    Sample: 7 - Steam Client
[2025-08-31 15:18:27] [INFO] -    Sample: 8 - winui2
[2025-08-31 15:18:27] [INFO] -    Sample: 10 - Counter-Strike
[2025-08-31 15:18:27] [INFO] -    Sample: 20 - Team Fortress Classic
[2025-08-31 15:18:29] [INFO] - Testing appdetails for appid: 730
[2025-08-31 15:18:29] [INFO] - ✅ appdetails successful: Counter-Strike 2
[2025-08-31 15:18:30] [INFO] - Testing rate limiting with consecutive requests on newer app IDs...
[2025-08-31 15:18:30] [INFO] - Request 1/10 - Testing AppID: 3990260
[2025-08-31 15:18:30] [INFO] - Testing appdetails for appid: 3990260
[2025-08-31 15:18:30] [INFO] - ✅ appdetails successful: GoobDemo
[2025-08-31 15:18:30] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:32] [INFO] - Request 2/10 - Testing AppID: 3990400
[2025-08-31 15:18:32] [INFO] - Testing appdetails for appid: 3990400
[2025-08-31 15:18:32] [INFO] - ✅ appdetails successful: Big BEAUTIFUL Van Derby Racing
[2025-08-31 15:18:32] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:33] [INFO] - Request 3/10 - Testing AppID: 3990870
[2025-08-31 15:18:33] [INFO] - Testing appdetails for appid: 3990870
[2025-08-31 15:18:34] [INFO] - ✅ appdetails successful: Replace the Lamp: The Last Shift
[2025-08-31 15:18:34] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:35] [INFO] - Request 4/10 - Testing AppID: 3991150
[2025-08-31 15:18:35] [INFO] - Testing appdetails for appid: 3991150
[2025-08-31 15:18:35] [INFO] - ✅ appdetails successful: Echoes of Vasteria Demo
[2025-08-31 15:18:35] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:37] [INFO] - Request 5/10 - Testing AppID: 3992880
[2025-08-31 15:18:37] [INFO] - Testing appdetails for appid: 3992880
[2025-08-31 15:18:37] [INFO] - ✅ appdetails successful: Rush Roulette Demo
[2025-08-31 15:18:37] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:38] [INFO] - Request 6/10 - Testing AppID: 3992900
[2025-08-31 15:18:38] [INFO] - Testing appdetails for appid: 3992900
[2025-08-31 15:18:38] [INFO] - ✅ appdetails successful: Hero of Sunset Demo
[2025-08-31 15:18:38] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:40] [INFO] - Request 7/10 - Testing AppID: 3993270
[2025-08-31 15:18:40] [INFO] - Testing appdetails for appid: 3993270
[2025-08-31 15:18:40] [INFO] - ✅ appdetails successful: Algoremind Demo
[2025-08-31 15:18:40] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:42] [INFO] - Request 8/10 - Testing AppID: 3994300
[2025-08-31 15:18:42] [INFO] - Testing appdetails for appid: 3994300
[2025-08-31 15:18:42] [INFO] - ✅ appdetails successful: Escape: Mall Demo
[2025-08-31 15:18:42] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:43] [INFO] - Request 9/10 - Testing AppID: 3995330
[2025-08-31 15:18:43] [INFO] - Testing appdetails for appid: 3995330
[2025-08-31 15:18:43] [INFO] - ✅ appdetails successful: 공고소녀(Gong GO Girl) Demo
[2025-08-31 15:18:43] [INFO] - Waiting 1.5s...
[2025-08-31 15:18:45] [INFO] - Request 10/10 - Testing AppID: 3996190
[2025-08-31 15:18:45] [INFO] - Testing appdetails for appid: 3996190
[2025-08-31 15:18:45] [INFO] - ✅ appdetails successful: Project: Haste Demo
[2025-08-31 15:18:45] [INFO] - --- Rate Limiting Test Complete ---
[2025-08-31 15:18:45] [INFO] -    10/10 successful requests
[2025-08-31 15:18:45] [INFO] -    14.7s elapsed
[2025-08-31 15:18:45] [INFO] -    Effective Rate: 40.9 requests/minute (with 1.5s delay)
[2025-08-31 15:18:45] [INFO] - ✅ Steam API Test Suite Complete```