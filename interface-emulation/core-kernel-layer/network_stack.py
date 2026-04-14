"""
WekezaOmniOS Interface Emulation — Network Stack
=================================================
Simulates a virtual network layer: interface registration, DNS
resolution, and ICMP echo (ping) emulation — all in memory.
"""

import hashlib


class NetworkStack:
    """
    In-memory simulation of a virtual network stack.

    Provides NIC registration, simulated DNS, and simulated ping.
    """

    def __init__(self):
        print("[NetworkStack] 🌐 Initialising virtual network stack...")
        self._interfaces: dict[str, dict] = {}
        print("[NetworkStack] ✅ Network stack ready.")

    # ------------------------------------------------------------------
    # Interface management
    # ------------------------------------------------------------------

    def add_interface(
        self, name: str, ip: str, netmask: str = "255.255.255.0"
    ) -> dict:
        """
        Registers a virtual network interface.

        Args:
            name (str): Interface name (e.g. 'eth0').
            ip (str): IP address string.
            netmask (str): Subnet mask (default '255.255.255.0').

        Returns:
            dict: The interface entry added.
        """
        entry = {"name": name, "ip": ip, "netmask": netmask, "state": "up"}
        self._interfaces[name] = entry
        print(
            f"[NetworkStack] Interface added: {name} → {ip}/{netmask}"
        )
        return entry

    def remove_interface(self, name: str) -> None:
        """
        Removes a registered network interface.

        Args:
            name (str): Interface name to remove.

        Raises:
            KeyError: If *name* is not registered.
        """
        if name not in self._interfaces:
            raise KeyError(f"[NetworkStack] Interface {name!r} not found.")
        del self._interfaces[name]
        print(f"[NetworkStack] Interface removed: {name}")

    def list_interfaces(self) -> list[dict]:
        """Returns a list of all registered interface dicts."""
        return list(self._interfaces.values())

    # ------------------------------------------------------------------
    # Network operations (simulated)
    # ------------------------------------------------------------------

    def ping(self, host: str) -> bool:
        """
        Simulates an ICMP echo request to *host*.

        Always returns True (simulated reachability).

        Args:
            host (str): Target hostname or IP address.

        Returns:
            bool: Always True.
        """
        print(
            f"[NetworkStack] PING {host}: 64 bytes from {host}: "
            "icmp_seq=1 ttl=64 time=0.1 ms"
        )
        return True

    def resolve(self, hostname: str) -> str:
        """
        Simulated DNS resolution.

        'localhost' resolves to '127.0.0.1'; everything else gets a
        deterministic fake IP derived from a hash of the hostname.

        Args:
            hostname (str): Hostname to resolve.

        Returns:
            str: IP address string.
        """
        if hostname in ("localhost", "127.0.0.1"):
            ip = "127.0.0.1"
        else:
            digest = hashlib.md5(hostname.encode()).hexdigest()
            # Build a fake routable IP in 10.x.x.x range
            a = int(digest[0:2], 16) % 256
            b = int(digest[2:4], 16) % 256
            c = int(digest[4:6], 16) % 256
            ip = f"10.{a}.{b}.{c}"
        print(f"[NetworkStack] DNS resolved: {hostname} → {ip}")
        return ip


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ns = NetworkStack()
    ns.add_interface("eth0", "192.168.1.10")
    ns.add_interface("lo", "127.0.0.1", "255.0.0.0")
    print(ns.list_interfaces())
    ns.ping("8.8.8.8")
    ns.resolve("localhost")
    ns.resolve("example.com")
    ns.remove_interface("eth0")
    print(ns.list_interfaces())
