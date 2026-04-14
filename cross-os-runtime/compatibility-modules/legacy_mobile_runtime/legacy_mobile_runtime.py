"""
WekezaOmniOS Legacy Mobile Runtime Module
Provides compatibility for legacy mobile platform binaries (pre-Android,
feature-phone OSes, early J2ME/BREW applications) inside the Cross-OS
Runtime Layer.

Supported legacy platforms:
- J2ME  (Java Micro Edition — MIDP/CLDC profiles)
- BREW  (Binary Runtime Environment for Wireless — Qualcomm)
- Symbian S60 / S40
- Windows Mobile 6.x
"""


# J2ME MIDP 2.0 → POSIX equivalents for common APIs
J2ME_TO_POSIX = {
    "javax.microedition.io.Connector.open": "open/connect",
    "javax.microedition.io.HttpConnection":  "socket+HTTP",
    "javax.microedition.rms.RecordStore":    "read/write (flat-file)",
    "javax.microedition.media.Player":       "ioctl (audio device)",
}

# Known legacy display resolutions → upscale factor to 1080p
DISPLAY_UPSCALE = {
    "128x128":  8.4,
    "176x208":  5.0,
    "240x320":  3.4,   # QVGA — very common J2ME target
    "320x240":  3.4,
    "360x640":  1.7,
}

SUPPORTED_PLATFORMS = ("j2me", "brew", "symbian", "windows_mobile")


class LegacyMobileRuntime:
    """
    Compatibility module for legacy mobile operating system applications.

    Responsibilities:
    - Identify the legacy platform from application metadata.
    - Translate legacy API calls to POSIX equivalents.
    - Upscale display parameters for modern screens.
    - Adapt the environment for emulated execution.
    """

    OS_NAME = "LegacyMobile"

    def __init__(self):
        print(f"[{self.OS_NAME}Runtime] Module loaded.")

    # ------------------------------------------------------------------
    # Platform identification
    # ------------------------------------------------------------------

    def detect_platform(self, app_metadata):
        """
        Infers the legacy platform from application metadata.

        Args:
            app_metadata (dict): Metadata from the application package,
                                 expected to contain a 'platform' key.

        Returns:
            str: Detected platform name or 'unknown'.
        """
        platform = app_metadata.get("platform", "unknown").lower()
        if platform not in SUPPORTED_PLATFORMS:
            print(
                f"[{self.OS_NAME}Runtime] ⚠️  Unknown platform "
                f"{platform!r}; will attempt best-effort emulation."
            )
        else:
            print(
                f"[{self.OS_NAME}Runtime] Detected platform: {platform}"
            )
        return platform

    # ------------------------------------------------------------------
    # API translation
    # ------------------------------------------------------------------

    def translate_api_call(self, legacy_api):
        """
        Maps a legacy mobile API call to its POSIX equivalent.

        Args:
            legacy_api (str): Legacy platform API identifier.

        Returns:
            str: POSIX equivalent or original string if unmapped.
        """
        posix_call = J2ME_TO_POSIX.get(legacy_api, legacy_api)
        print(
            f"[{self.OS_NAME}Runtime] API translation: "
            f"{legacy_api!r} → {posix_call!r}"
        )
        return posix_call

    # ------------------------------------------------------------------
    # Display upscaling
    # ------------------------------------------------------------------

    def upscale_display(self, original_resolution):
        """
        Returns the upscale factor needed to render a legacy app on a
        modern display.

        Args:
            original_resolution (str): Resolution string, e.g. '240x320'.

        Returns:
            float: Upscale multiplier.
        """
        factor = DISPLAY_UPSCALE.get(original_resolution, 1.0)
        print(
            f"[{self.OS_NAME}Runtime] Display upscale for "
            f"{original_resolution!r}: ×{factor}"
        )
        return factor

    # ------------------------------------------------------------------
    # Environment adaptation
    # ------------------------------------------------------------------

    def adapt_environment(self, env_vars, platform="j2me"):
        """
        Injects platform-appropriate environment variables.

        Args:
            env_vars (dict): Original environment dictionary.
            platform (str): Target legacy platform.

        Returns:
            dict: Adapted environment dictionary.
        """
        adapted = dict(env_vars)
        adapted["OS_TYPE"]       = "legacy_mobile"
        adapted["LEGACY_PLATFORM"] = platform
        adapted.setdefault("HOME",   "/midlet")
        adapted.setdefault("TMPDIR", "/tmp/legacy")
        print(
            f"[{self.OS_NAME}Runtime] Environment adapted "
            f"for platform={platform!r}."
        )
        return adapted

    # ------------------------------------------------------------------
    # State translation
    # ------------------------------------------------------------------

    def translate_process_state(self, snapshot):
        """
        Converts a legacy mobile application snapshot into the universal
        runtime format.

        Args:
            snapshot (dict): Raw legacy process state.

        Returns:
            dict: Universal process state.
        """
        state = snapshot.copy()
        platform = self.detect_platform(state.get("app_metadata", {}))
        state["source_os"]  = "legacy_mobile"
        state["platform"]   = platform

        if "display_resolution" in state:
            state["upscale_factor"] = self.upscale_display(
                state["display_resolution"]
            )

        if "api_calls" in state:
            state["api_calls"] = [
                self.translate_api_call(c) for c in state["api_calls"]
            ]

        if "env" in state:
            state["env"] = self.adapt_environment(state["env"], platform)

        print(f"[{self.OS_NAME}Runtime] Process state translated.")
        return state


# ---------------------------------------------------------------------------
# Demo
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    runtime = LegacyMobileRuntime()

    runtime.detect_platform({"platform": "j2me"})
    runtime.translate_api_call("javax.microedition.io.Connector.open")
    runtime.upscale_display("240x320")

    snapshot = {
        "pid": 7001,
        "app_metadata": {"platform": "j2me", "midlet_name": "SnakeGame"},
        "display_resolution": "128x128",
        "api_calls": [
            "javax.microedition.rms.RecordStore",
            "javax.microedition.media.Player",
        ],
        "env": {},
        "app_state": {"level": 3, "score": 1200},
    }
    import json
    translated = runtime.translate_process_state(snapshot)
    print(json.dumps(translated, indent=2))
