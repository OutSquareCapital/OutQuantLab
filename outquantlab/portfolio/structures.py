from outquantlab.indicators import GenericIndic

def get_categories_dict(asset_names: list[str], indics: list[GenericIndic]) -> list[dict[str, str]]:
    return [
        {"assets": asset_name, "indics": indic.name, "params": param_name}
        for indic in indics
        for param_name in indic.get_combo_names()
        for asset_name in asset_names
    ]
