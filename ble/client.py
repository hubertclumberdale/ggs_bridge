import json

from bleak import BleakClient

from ble.assembler import JsonAssembler


UUID_NOTIFY = "0000ff01-0000-1000-8000-00805f9b34fb"
UUID_WRITE = "0000ff02-0000-1000-8000-00805f9b34fb"


class GGSClient:

    def __init__(self, address):

        self.address = address
        self.client = BleakClient(address)

        self.assembler = JsonAssembler()

    async def connect(self):

        await self.client.connect()

        print(f"[BLE] Connected: {self.address}")

        await self.client.start_notify(
            UUID_NOTIFY,
            self._notification_handler
        )

    async def disconnect(self):

        if self.client.is_connected:
            await self.client.disconnect()

    async def get_status(self):

        cmd = {
            "method": "getDevSta"
        }

        await self.write_json(cmd)

    async def write_json(self, payload):

        data = json.dumps(
            payload,
            separators=(",", ":")
        ).encode()

        await self.client.write_gatt_char(
            UUID_WRITE,
            data,
            response=True
        )

        print("[WRITE]", data.decode())

    def _notification_handler(self, sender, data):

        try:
            text = data.decode(
                "utf-8",
                errors="ignore"
            )

        except Exception:
            return

        obj = self.assembler.feed(text)

        if obj is not None:

            print("\n===== GGS DATA =====")
            print(
                json.dumps(
                    obj,
                    indent=2,
                    ensure_ascii=False
                )
            )
            print("====================\n")