# UniBa_Tesi


dato un oggetto recuperare le tecniche correlate a quell'oggetto  
data una tecnica recuperare le tecniche correlate a oggetti in cui è presente la tecnica iniziale  
dividerle tra le tattiche e capire quelle future o precedenti  

# COSE DA FARE:
- Per ogni Campaign e Tool registrare gli id delle Technique collegate usare get_objects_using_technique_id (nella classe astratta AbstractObjectWithTechniquesRetriever
implementare l'assegnazione degli id degli AttackPattern nella tuple)
- Creare in AttackPatternContainer un metodo che vada a usare gli altri 2 Container salvando in una lista gli id degli AttackPattern che 
sono presenti nel Tool o Campaign
- Creare in AttackPatternContainer un metodo privato che data una lista di id di AttackPattern li fa diventare un set e restituisce una lista di oggetti AttackPattern
- Per ogni Technique aggiungere attributi Mitigation e Detection
- Valuta se per ogni tecnica ha senso registrare i DataComponent
- Implementare i meccanismi di logica per ottenere le Techniques per ogni KillChainPhase