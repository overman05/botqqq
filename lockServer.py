from typing import Dict
import requests


class LoginError(Exception):
    def __init__(self, text):
        self.txt = text


class LockerAPI:
    server: str
    cookie: dict

    def __init__(self, server, login, password):
        self.server = server
        self._login(login, password)

    def get_version(self):
        rv = requests.get(self.server + "/api/GetVersion")

        assert rv.status_code == 200, f"Returned {rv.json()}"
        return rv.json()["version"]

    def _login(self, login, password):
        rv = requests.post(
            self.server + "/api/Login", json={"login": login, "password": password}
        )

        resp = rv.json()
        if resp["status"] == True:
            cookie = {f"{resp['session']['name']}": f"{resp['session']['value']}"}
            self.cookie = cookie
            return
        else:
            raise LoginError("Не удалось подключиться к серверам вальв")

    def get_cells(self, device_id=None):
        rv = requests.post(
            self.server + "/api/GetCells",
            cookies=self.cookie,
            json={"device_id": device_id} if device_id is not None else None,
        )
        assert rv.status_code == 200, f"GetCells failed: {rv.json()}"

        return rv.json()

    def get_devices(self):
        rv = requests.post(self.server + "/api/GetDevices", cookies=self.cookie)
        assert rv.status_code == 200, f"GetCells failed: {rv.json()}"

        return rv.json()

    def device_location(self):
        rv = requests.post(
            self.server + "/api/GetDeviceLocations",
            cookies=self.cookie
            # json={"device_id": "1"},
        )
        assert rv.status_code == 200, f"GetCells failed: {rv.json()}"

        return rv.json()

    def occupy_cell(self, device_id):
        rv = requests.post(
            self.server + "/api/OccupyCell",
            cookies=self.cookie,
            json={"device_id": device_id},
        )
        assert rv.status_code == 200, f"OccupyCell failded: {rv.json()}"
        return rv.json()

    def free_cell(self, cell_id):
        rv = requests.post(
            self.server + "/api/FreeCell",
            cookies=self.cookie,
            json={"cell_id": cell_id},
        )
        return rv.json()

    def logout(self):
        requests.post(self.server + "/api/Logout")
