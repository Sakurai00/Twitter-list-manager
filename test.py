import list_manager

#list_manager.create_list()

# ==========================================================

def create_list() -> int:
    """ 指定された名前のリストを作成する

    Returns:
        int: List ID
    """

    l = list_manager.api.create_list(name = "test", mode = "private")
    return l.id

create_list()