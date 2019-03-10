def is_external_image(path):
    stripped_path = path.strip()
    stripped_lower_case_path = stripped_path.lower()
    if stripped_lower_case_path.startswith("http://") or stripped_lower_case_path.startswith("https://"):
        return True
    else:
        return False
