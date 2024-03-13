import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

# download and parse ATT&CK STIX data
attackdata = attackToExcel.get_stix_data("enterprise-attack")
print(attackdata)
techniques_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
#print(techniques_data)

# show T1102 and sub-techniques of T1102
techniques_df = techniques_data["techniques"]
#print(techniques_df[techniques_df["ID"].str.contains("T1102")]["name"])
# 512                                 Web Service
# 38     Web Service: Bidirectional Communication
# 121             Web Service: Dead Drop Resolver
# 323          Web Service: One-Way Communication
# Name: name, dtype: object

# show citation data for LOLBAS Wmic reference
citations_df = techniques_data["citations"]
#print(citations_df[citations_df["reference"].str.contains("LOLBAS Wmic")])
#         reference                                           citation                                                url
# 1010  LOLBAS Wmic  LOLBAS. (n.d.). Wmic.exe. Retrieved July 31, 2...  https://lolbas-project.github.io/lolbas/Binari...