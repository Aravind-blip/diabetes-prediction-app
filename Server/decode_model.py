import base64
from pathlib import Path

def main():
    artifacts_dir = Path(__file__).parent / "artifacts"
    b64_path = artifacts_dir / "DCM.pickle.base64"
    pickle_path = artifacts_dir / "DCM.pickle"

    if not b64_path.exists():
        raise FileNotFoundError(f"Base64 file not found: {b64_path}")

    data = b64_path.read_text().strip()
    binary = base64.b64decode(data)

    pickle_path.write_bytes(binary)
    print(f"Created pickle model at: {pickle_path}")

if __name__ == "__main__":
    main()
