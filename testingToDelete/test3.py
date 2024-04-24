from src.model.container import AttackPatternsContainer, AssetContainer

print(AssetContainer().get_data()[0].external_references)

for obj in AssetContainer().get_data():
    for er in obj.external_references:
        if '/assets/' in er.url and 'mitre-' in er.source_name:
            print(er.external_id)
            break
        print('n/a')