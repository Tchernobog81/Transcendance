# 🌌 CHANGELOG - TRANSCENDANCE

## [Beta 1.0.7] - 2026-01-30
### Fix
- **Core :** Ajout d'un 'Master Bypass' (sécurité 4s) pour garantir le déblocage de l'UI même en cas d'erreur de script.
- **Graph :** Initialisation protégée par try/catch pour éviter l'arrêt du JS si les plugins CDN sont lents.
- **Git :** Wrapper PowerShell pour masquer les fausses erreurs NativeCommandError de Git.