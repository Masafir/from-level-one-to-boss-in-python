# 🎮 Mini-Projet : Game Analytics Pipeline Async

## Objectif

Construis un **pipeline de traitement d'événements de jeu en temps réel** avec asyncio.

## Architecture

```
[Event Generator] → [Queue] → [Router] → [Handlers]
                                    ↓
                              [Stats Aggregator]
                                    ↓
                              [Dashboard Output]
```

## Critères de réussite ✅

- [ ] Producer : génère 1000+ événements variés
- [ ] Consumer pool : 5 workers en parallèle
- [ ] Router : dispatche vers les bons handlers par type
- [ ] Stats : agrège kills, scores, items en temps réel
- [ ] Rate limiter : max 100 events/sec
- [ ] Retry : les handlers échouent aléatoirement (5%), retry avec backoff
- [ ] Circuit breaker : si trop d'erreurs, le handler est désactivé
- [ ] Output : affiche un dashboard final avec stats
