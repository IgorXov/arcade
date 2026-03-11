import json
from pathlib import Path

STATS_FILE = Path(__file__).parent / "stats.json"

stats = {
    "wins": 0,
    "losses": 0,
    "battle_wins": 0,
    "battle_losses": 0,
    "level1_wins": 0,
    "level1_losses": 0,
    "level2_wins": 0,
    "level2_losses": 0,
    "level3_wins": 0,
    "level3_losses": 0,
    "level4_wins": 0,
    "level4_losses": 0,
    "level5_wins": 0,
    "level5_losses": 0,
    "level6_wins": 0,
    "level6_losses": 0,
    "level7_wins": 0,
    "level7_losses": 0,
    "current_win_streak": 0,
    "best_win_streak": 0,
    "best_survival": 0.0,
    "total_runs": 0,
}


def _load():
    if not STATS_FILE.exists():
        return
    try:
        data = json.loads(STATS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return
    if isinstance(data, dict):
        for key in stats:
            if key in data and isinstance(data[key], (int, float)):
                stats[key] = data[key]


def _save():
    try:
        STATS_FILE.write_text(json.dumps(stats, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass


_load()


def _mode_keys(mode: str):
    return f"{mode}_wins", f"{mode}_losses"


def record_result(mode: str, won: bool, survived_time: float):
    stats["total_runs"] += 1

    if survived_time > stats["best_survival"]:
        stats["best_survival"] = survived_time

    if won:
        stats["wins"] += 1
        stats["current_win_streak"] += 1
        if stats["current_win_streak"] > stats["best_win_streak"]:
            stats["best_win_streak"] = stats["current_win_streak"]
        win_key, _ = _mode_keys(mode)
        if win_key in stats:
            stats[win_key] += 1
    else:
        stats["losses"] += 1
        stats["current_win_streak"] = 0
        _, loss_key = _mode_keys(mode)
        if loss_key in stats:
            stats[loss_key] += 1

    _save()


def record_win(mode: str, survived_time: float):
    record_result(mode, True, survived_time)


def record_loss(mode: str, survived_time: float):
    record_result(mode, False, survived_time)


def get_stats_lines():
    return [
        f"Wins: {stats['wins']}  Losses: {stats['losses']}  Runs: {stats['total_runs']}",
        f"Win streak: {stats['current_win_streak']}  Best: {stats['best_win_streak']}",
        f"Best survival: {stats['best_survival']:.1f}s",
    ]