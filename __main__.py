from src.mediators.app_mediator import AppMediator


def main():
    AppMediator().read_args().read_configs().run_bot()


if __name__ == "__main__":
    main()
