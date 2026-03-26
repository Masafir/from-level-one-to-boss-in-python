# 🎮 Mini-Projet : API de Jeu Multijoueur Sécurisée

## Objectif

Construis une API de jeu multijoueur avec un système d'authentification complet, RBAC, et des patterns backend avancés.

## Fonctionnalités

1. **Auth** : Register, login, JWT, refresh tokens
2. **RBAC** : player, moderator, admin
3. **Rate Limiting** : 60 req/min par user
4. **Event Bus** : log tous les événements importants
5. **Background Tasks** : emails, calculs de stats

## Critères de réussite ✅

- [ ] Register + Login avec JWT
- [ ] Hashing bcrypt des mots de passe
- [ ] Middleware d'authentification
- [ ] 3 rôles avec permissions différentes
- [ ] Rate limiter intégré
- [ ] Event bus pour les notifications
- [ ] Background tasks pour l'onboarding
- [ ] Tests avec auth (au moins 10 tests)
