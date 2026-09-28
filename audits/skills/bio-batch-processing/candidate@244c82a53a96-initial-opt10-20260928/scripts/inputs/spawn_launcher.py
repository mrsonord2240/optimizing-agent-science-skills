import multiprocessing


if __name__ == "__main__":
    multiprocessing.set_start_method("spawn")
    import multiprocessing_recipe  # noqa: F401,E402
