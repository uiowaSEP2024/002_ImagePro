import pyorthanc
import time
import os


def test_ping_orthanc(orthanc_url):
    try:
        orthanc = pyorthanc.Orthanc(orthanc_url)
        print(
            f"Connected to orthanc at {orthanc_url}"
            f" with tools {orthanc.get_tools()}"
        )
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Ping Orthanc server")
    # parser.add_argument("-u", "orthanc_url", type=str, help="URL of the Orthanc server")
    # args = parser.parse_args()
    orthanc_url = os.environ.get("ORTHANC_URL")
    print(f"Orthanc URL: {orthanc_url}")
    import logging

    logging.basicConfig(level=logging.INFO)
    while True:
        test_ping_orthanc(orthanc_url)
        print("Sleeping for 60 seconds")
        logging.info("Sleeping for 60 seconds")
        time.sleep(60)
