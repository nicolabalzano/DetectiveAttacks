from pathlib import Path

import mitreattack.attackToExcel.attackToExcel as attackToExcel
import mitreattack.attackToExcel.stixToDf as stixToDf

from pathlib import Path


def check_excel_files_exist(excel_folder: Path, domain: str):
    files_to_check = [
        f"{domain}.xlsx",
        f"{domain}-datasources.xlsx",
        f"{domain}-campaigns.xlsx",
        f"{domain}-groups.xlsx",
        f"{domain}-matrices.xlsx",
        f"{domain}-mitigations.xlsx",
        f"{domain}-relationships.xlsx",
        f"{domain}-software.xlsx",
        f"{domain}-tactics.xlsx",
        f"{domain}-techniques.xlsx",
    ]

    for file_name in files_to_check:
        if not (excel_folder / file_name).exists():
            raise FileNotFoundError(f"File not found: {file_name}")


# check files xlxs exists
try:
    check_excel_files_exist(Path.cwd() / "enterprise-attack", "enterprise-attack")
    print("ALL FILES EXISTS")
except FileNotFoundError as e:
    print(e)





# download and parse ATT&CK STIX data
attackdata = attackToExcel.get_stix_data("enterprise-attack")
# print(attackdata)
enterprise_df_data = stixToDf.techniquesToDf(attackdata, "enterprise-attack")
print(enterprise_df_data)

# show T1102 and sub-techniques of T1102
techniques_df = enterprise_df_data["techniques"]
# print(techniques_df[techniques_df["ID"].str.contains("T1102")]["name"])

# show citation data for LOLBAS Wmic reference
citations_df = enterprise_df_data["citations"]
print(citations_df[citations_df["url"].str.contains("https")])

# in pratica è
# nome_categoria = techniques, procedure examples, associated mitigations, citations
# nome_categoria_df = enterprise_df_data["nome_categoria"]
# nome_categoria_df["nome_colonna"].vari_filtri