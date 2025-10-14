
def print_render_info_start(filename: str) -> None:
    if filename is not None:
        print(f"Info: Started rendering '{filename}'...")
    else:
        print("Info: Started rendering...")


def print_render_info_end(filename: str, ellapsed_time: float) -> None:
    if filename is not None:
        print(f"Info: Rendering of '{filename}' completed in {ellapsed_time:.2f} seconds.")
    else:
        print(f"Info: Rendering completed in {end_time - start_time:.2f} seconds.")

