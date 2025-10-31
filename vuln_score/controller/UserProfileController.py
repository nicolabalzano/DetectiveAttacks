import model.Dao as db


def _get_assets() -> list:
    return db.read_assets()


def _update_assets(assets: list) -> dict:
    try:
        for asset in assets:
            db.update_asset_score(asset['id'], asset['score'])
    except:
        raise SystemError('Something went wrong while updating assets')
    return {'status': 200}
