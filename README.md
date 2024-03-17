# UniBa_Tesi


dato un oggetto recuperare le tecniche correlate a quell'oggetto  
data una tecnica recuperare le tecniche correlate a oggetti in cui è presente la tecnica iniziale  
dividerle tra le tattiche e capire quelle future o precedenti  

# COSE DA FARE:
- eliminare STIXBase20 perchè non serve a nulla non facendo le classi frozen e capire se serve definire i propetry con le dataclass per lgi attributi da rendere privati/protected
- fare le robe per ottenere un set di AttackPatterns tramite un AttackPattern
- Mettere tutti gli attributi privati/protected e sitemare tutti i commenti in inglese
- Per ogni Technique aggiungere attributi Mitigation e Detection
- Valuta se per ogni tecnica ha senso registrare i DataComponent
- Implementare i meccanismi di logica per ottenere le Techniques per ogni KillChainPhase