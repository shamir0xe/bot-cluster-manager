from src.mediators.app_mediator import AppMediator


def main():
    AppMediator().read_args().read_configs().run_bot()


if __name__ == "__main__":
    main()
    # asyncio.ensure_future(main())
    # asyncio.run(main())
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(asyncio.wait([loop.create_task(main())]))
    # loop.close()
