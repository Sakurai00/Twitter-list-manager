import list_manager, twapi

#list_manager.create_list()

# ==========================================================

#list_manager.diff_of_csv("@Halfas24_list-15428.csv", "@Sakurai_Absol_illustrator.csv")

api = twapi.generate_api()

api.update_status("test")