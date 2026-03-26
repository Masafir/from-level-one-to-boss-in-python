# 🌊 Mini-Projet : Streaming de Logs de Combat

## Objectif

Construis un pipeline de streaming complet (Event-Driven) qui analyse un flux infini d'événements de combat en temps réel, affiche des alertes (Trophées), et calcule un DPS (Damage Per Second) global en utilisant une fenêtre temporelle (Tumbling Window).

## Architecture 

1. **Producer (`game_server`)** : Génère entre 1 et 5 événements aléatoires par seconde.
   - Event: `{"player": "Bob", "target": "Orc", "damage": 50, "is_crit": False}`
2. **MessageBroker** : Reçoit ces événements et les dispatche ("Fan-out").
3. **Consumer 1 (`trophy_service`)** : Écoute les events individuels. Si `damage > 500` ET `is_crit == True`, affiche une alerte `🏆 MEGA CRIT par [Player] !`.
4. **Consumer 2 (`dps_meter`)** : Écoute le flux pour calculer le DPS global du serveur !
   - Aggrège les dégâts pendant 5 secondes (Tumbling Window).
   - Affiche `📊 Server DPS (Last 5s): [dps] dégats/sec`.

## Critères de réussite ✅

- [ ] Tout tourne avec `asyncio` (`gather`, Queues...).
- [ ] Le broker distribue correctement aux deux services (Fan-out).
- [ ] Le `trophy_service` traite un par un sans bloquer.
- [ ] Le `dps_meter` utilise correctement le temps (time.time()) pour isoler les tranches de 5 secondes.
- [ ] Le script ne crashe jamais et tourne indéfiniment jusqu'à interruption manuelle (`Ctrl+C`).
