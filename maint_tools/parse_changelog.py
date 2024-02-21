from datetime import datetime, timezone
import sys
import re
from pathlib import Path
from argparse import ArgumentParser


def parse_changelog(changelog_content: str) -> dict:
    version_re = re.compile(r"## \[([\w\.]+)\]")

    matches = list(version_re.finditer(changelog_content))
    starts = [m.start() for m in matches]
    splits = [[start, end] for start, end in zip(starts, starts[1:] + [None])]

    def _strip_first_line(content: str) -> str:
        lines = content.splitlines()
        return "\n".join(lines[1:]).strip()

    return {
        match.group(1): _strip_first_line(changelog_content[start:end].strip())
        for match, (start, end) in zip(matches, splits)
    }


def update_date_in_changelog(changelog_content: str, version: str) -> str:
    current_time = datetime.now(timezone.utc)
    lines = changelog_content.splitlines()

    output_lines = []
    for line in lines:
        if line.startswith(f"## [{version}]"):
            date_str = current_time.strftime("%Y-%m-%d")
            output_lines.append(f"## [{version}] - {date_str}")
        else:
            output_lines.append(line)
    return "\n".join(output_lines)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("changelog_file", type=Path)
    parser.add_argument("version")
    parser.add_argument(
        "--only-check", action="store_true", help="Check if version exists in changelog"
    )

    args = parser.parse_args()

    assert args.changelog_file.exists()

    changelog_content = args.changelog_file.read_text()

    changelog = parse_changelog(changelog_content)

    version_match = re.match(r"(\d+\.\d+\.\d+)", args.version)
    release_version = version_match.group(1)

    if release_version not in changelog:
        print(f"{release_version} is not in changelog! Add changelog items to continue")
        sys.exit(1)

    if args.only_check:
        print(f"Check successful: {release_version} is in changelog")
        sys.exit(0)

    # Update date in changelog and print changelog items
    new_changelog = update_date_in_changelog(changelog_content, release_version)
    args.changelog_file.write_text(new_changelog)

    print(changelog[release_version])
