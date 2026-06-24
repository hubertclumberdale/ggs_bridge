import asyncio
import yaml

from ble.client import GGSClient


async def main():

    with open("config.yaml", "r") as f:
        cfg = yaml.safe_load(f)

    ggs = GGSClient(
        cfg["ble"]["address"]
    )

    await ggs.connect()

    await ggs.get_status()

    while True:
        await asyncio.sleep(30)

        try:
            await ggs.get_status()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    asyncio.run(main())