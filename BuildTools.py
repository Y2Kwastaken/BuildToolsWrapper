import requests
import subprocess
import argparse
from tqdm import tqdm
import shutil
import os

LATEST = "1.19.3"
BUILD_TOOLS_NAME = "BuildTools.jar"
BUILD_TOOLS_LOG_NAME = "BuildTools.log.txt"
BUILD_TOOLS_URL = "https://hub.spigotmc.org/jenkins/job/BuildTools/lastSuccessfulBuild/artifact/target/BuildTools.jar"
ABSOLUTE_PATH = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = ABSOLUTE_PATH + "/cache"
TEMP_PATH = ABSOLUTE_PATH + "/tmp"
BTOOLS_LOGS_PATH = CACHE_PATH + "/logs"


def is_cached(file_name: str):
    if not os.path.exists(CACHE_PATH):
        os.mkdir(CACHE_PATH)
    return os.path.exists(CACHE_PATH + "/" + file_name)


def create_temp_dir():
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)


def clear_cache():
    print("Clearing caches...")
    if os.path.exists(CACHE_PATH):
        shutil.rmtree(CACHE_PATH)
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)


def download_build_tools():
    download_stream = requests.get(BUILD_TOOLS_URL, stream=True)
    total_size = int(download_stream.headers.get("content-length", 0))
    block_size = 1024

    with open(CACHE_PATH + "/" + BUILD_TOOLS_NAME, "wb") as file:
        for data in tqdm(download_stream.iter_content(block_size), total=total_size / block_size, unit="KB", unit_scale=True):
            file.write(data)


def run_build_tools(args: list):
    create_temp_dir()
    shutil.copyfile(CACHE_PATH + "/" + BUILD_TOOLS_NAME,
                    TEMP_PATH + "/" + BUILD_TOOLS_NAME)
    subprocess.run(["java", "-jar", BUILD_TOOLS_NAME, *args],
                   cwd=TEMP_PATH)
    print("BuildTools finished running. cleaning up...")
    # Find the jar that starts with "spigot"
    tmp_files: list[str] = os.listdir(TEMP_PATH)
    server_jar: str = ""
    for file in tmp_files:
        if file.startswith("spigot"):
            server_jar = file
            break

    shutil.move(TEMP_PATH + "/" + server_jar,
                CACHE_PATH + "/" + server_jar)

    if not os.path.exists(BTOOLS_LOGS_PATH):
        os.mkdir(BTOOLS_LOGS_PATH)

    shutil.move(TEMP_PATH + "/" + BUILD_TOOLS_LOG_NAME,
                BTOOLS_LOGS_PATH + "/" + BUILD_TOOLS_LOG_NAME)

    shutil.rmtree(TEMP_PATH)


def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="BuildTools wrapper")

    parser.add_argument(
        '--version',
        '-v',
        default=LATEST,
        action='store',
        help='The version of spigot to build')
    parser.add_argument(
        '--clear-cache',
        '-c',
        action='store_true',
        help="Clears the cache of BuildTools and the server jar"
    )
    parser.add_argument(
        '--remapped',
        '-r',
        action="store_true",
        help="Builds a remapped jar"
    )
    parser.add_argument(
        '--output-dir',
        '-o',
        default='.',
        action='store',
        help="The directory to output the server jar to"
    )
    parser.add_argument(
        '--ignore-cache',
        action='store_true',
        help='Ignores the cache and downloads and runs BuildTools for the specified version anyways'
    )

    args = parser.parse_args()
    run_args = ['--rev', args.version]

    if (args.clear_cache):
        clear_cache()
        return

    if args.remapped:
        run_args.append("--remapped")

    if not is_cached(BUILD_TOOLS_NAME):
        download_build_tools()

    # absolute path
    print(os.path.abspath(args.output_dir))

    if not is_cached("spigot-" + args.version + ".jar") or args.ignore_cache:
        run_build_tools(["--rev", args.version])

    shutil.copy(CACHE_PATH + "/spigot-" + args.version + ".jar",
                args.output_dir + "/spigot-" + args.version + ".jar")


if __name__ == "__main__":
    main()
